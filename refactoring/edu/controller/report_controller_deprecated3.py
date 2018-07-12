import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.config.first_row_config as first_row_config
import refactoring.edu.config.report_config as report_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao

import numpy as np

school_ids, school_names = report_config.get_school_info()
district_ids, district_names = report_config.get_district_info()
subject_ids, subject_names = report_config.get_subject_info()

exam_id = report_config.exam.exam_id
exam_where = qa.Where("examId", exam_id)
district_where = qa.Where("districtId")
school_where = qa.Where("schoolId")
subject_where = qa.Where("subjectId")
class_where = qa.Where('classId')

DISTRICT_CODE = 1
SCHOOL_CODE = 2

DIMEN_CODE = 1
SUM_CODE = 2

district_len = len(district_ids)
school_len = len(school_ids)


def get_std_names(index):
    result = []
    for i in range(school_len):
        if i == index:
            result.append(school_names[index])
        else:
            result.append("学校%d" % (i + 1))
    return result


def get_subject_id_by_name(subject_name):
    return subject_ids[subject_names.index(subject_name)]


def get_ranges(start, end, step):
    ids = []
    names = []
    scopes = range(start, end, step)
    for index, scope in enumerate(scopes[0:-1]):
        ids.append([scope, scopes[index + 1]])
        names.append("(%d, %d]" % (scope, scopes[index + 1]))
    if scopes[-1] < end:
        ids.append([scopes[-1], end])
        names.append("(%d, %d]" % (scopes[-1], end))
    return ids, names


def get_distributions(subject_name):
    distributions = report_config.get_distribution(subject_name)
    ids = []
    names = []
    for distribution in distributions[1]:
        ids_t, names_t = get_ranges(distribution[0], distribution[1], distribution[2])
        ids.extend(ids_t)
        names.extend(names_t)
    if distributions[0] == report_config.ALL:
        start = distributions[1][0][0]
        step = distributions[1][0][2]
        names[0] = "[%d, %d]" % (start, start + step)
    return ids, names


def get_names(title_extra, table_code, district_code):
    if title_extra:
        extra_title = report_config.get_table_extra_title(table_code)
        if district_code == DISTRICT_CODE:
            return list_util.add_something_to_list(
                extra_title, district_names)
        elif district_code == SCHOOL_CODE:
            return list_util.add_something_to_list(
                extra_title, school_names)
    else:
        if district_code == DISTRICT_CODE:
            return district_names
        elif district_code == SCHOOL_CODE:
            return school_names


def get_table_where_ids(table_code, district_code, subject_code):
    if district_code == DISTRICT_CODE:
        if subject_code == DIMEN_CODE:
            table = table_config.get_district_dimen_table(table_code)
        elif subject_code == SUM_CODE:
            table = table_config.get_district_sum_table(table_code)

        varied_where = district_where
        ids = district_ids
    elif district_code == SCHOOL_CODE:
        if subject_code == DIMEN_CODE:
            table = table_config.get_school_dimen_table(table_code)
        elif subject_code == SUM_CODE:
            table = table_config.get_school_sum_table(table_code)

        varied_where = school_where
        ids = school_ids
    return table, varied_where, ids


def get_subject_rows(item, table_code, district_code, title_extra=True):
    table, varied_where, ids = get_table_where_ids(table_code, district_code, DIMEN_CODE)
    subject_cell = qa.CellWithOrders(item, table, [varied_where, exam_where], "subjectId", subject_ids)
    subject_row = qa.ColSeriesCell(subject_cell, ids)
    return list_util.combine_values_by_col(get_names(title_extra, table_code, district_code),
                                           subject_row.get_values())


def get_subject_sum_rows(item, table_code, district_code):
    subject_row = get_subject_rows(item, table_code, district_code)

    table, varied_where, ids = get_table_where_ids(table_code, district_code, SUM_CODE)
    sum_cell = qa.Cell(item, table, [varied_where, exam_where])
    sum_row = qa.ColSeriesCell(sum_cell, ids)
    return list_util.combine_values_by_col(subject_row, sum_row.get_values())


def get_district_sum_line_of_rows(item, type_code):
    if type_code == report_config.SPECIAL:
        table = table_config.QA_SCHOOL_LINE_TABLE
    elif type_code == report_config.CURRENT:
        table = table_config.QA_ZK_SCHOOL_LINE_TABLE
    varied_where = school_where
    line_cell = qa.Cell(item, table, [varied_where, exam_where])
    line_row = qa.ColSeriesCell(line_cell, school_ids)
    return list_util.combine_values_by_col(school_names, line_row.get_values())


def get_district_subject_distribution_values(subject_name, ids, table_code):
    distribution = report_config.get_distribution(subject_name)
    statistics_type = distribution[0]

    greater_where = qa.Where("sum", symbol=">")
    less_equal_where = qa.Where("sum", symbol="<=")

    basic_where = [exam_where]
    if subject_name == "总分":
        dimen_table = table_config.get_stu_sum_table(table_code)
        if statistics_type == report_config.COUNT:
            basic_where.append(qa.Where("count", value=distribution[2]))
    else:
        dimen_table = table_config.get_stu_dimen_table(table_code)
        subject_where.value = get_subject_id_by_name(subject_name)
        basic_where.append(subject_where)

    normal_cell = qa.Cell("COUNT(*)", dimen_table, [[greater_where, less_equal_where]] + basic_where)
    if statistics_type == report_config.ALL:
        greater_equal_where = qa.Where("sum", symbol=">=")
        extra_cell = qa.Cell("COUNT(*)", dimen_table, [[greater_equal_where, less_equal_where]] + basic_where)
        row1 = qa.RowSeriesCell(extra_cell, ids[0:1])
        row2 = qa.RowSeriesCell(normal_cell, ids[1:])
        return qa.DataRows.combine_col_rows(row1, row2)
    else:
        row = qa.RowSeriesCell(normal_cell, ids)
        return row.get_values()


def get_district_subject_std_values(subject_name, table_code):
    wheres = [school_where, exam_where]
    if subject_name == "总分":
        stu_table = table_config.get_stu_sum_table(table_code)
        school_table = table_config.get_school_sum_table(table_code)
    else:
        stu_table = table_config.get_stu_dimen_table(table_code)
        school_table = table_config.get_school_dimen_table(table_code)

        subject_where.set_value(get_subject_id_by_name(subject_name))
        wheres.append(subject_where)

    subject_total = report_config.get_total(subject_name)

    xresult = []
    yresult = []

    school_subject_num_cell = qa.Cell("num_nz", school_table, wheres)
    school_subject_num_row = qa.RowSeriesCell(school_subject_num_cell, school_ids)

    school_subject_avg_cell = qa.Cell("avg", school_table, wheres)
    stu_subject_sum_cell = qa.Cell("sum", stu_table, wheres)
    for school_id in school_ids:
        school_where.set_value(school_id)
        xresult.append(round(school_subject_avg_cell.get_value() / subject_total, 2))
        yresult.append(round(np.std(stu_subject_sum_cell.get_row_values(), ddof=1), 2))
    num = school_subject_num_row.get_values()[0]
    return xresult, yresult, num


def get_district_subject_box_values(subject_name, table_code):
    wheres = [school_where, exam_where]
    if subject_name == "总分":
        stu_table = table_config.get_stu_sum_table(table_code)
    else:
        stu_table = table_config.get_stu_dimen_table(table_code)
        subject_where.set_value(get_subject_id_by_name(subject_name))
        wheres.append(subject_where)
    stu_subject_sum_cell = qa.Cell("sum", stu_table, wheres)
    stu_subject_sum_row = qa.ColSeriesCell(stu_subject_sum_cell, school_ids)
    return stu_subject_sum_row.get_values()


def print_rows(rows):
    for row in rows:
        print(row)


def district_avg_rank_of_subject_sum_table(base_student):
    district_rows1 = get_subject_sum_rows(item_config.AVG_NULL_ITEM, table_config.QA, DISTRICT_CODE)
    school_rows1 = get_subject_sum_rows(item_config.AVG_RANK_ITEM, table_config.QA, SCHOOL_CODE)
    result = district_rows1 + school_rows1

    if base_student == report_config.SPECIAL:
        district_rows2 = get_subject_sum_rows(item_config.AVG_NULL_ITEM, table_config.QA_ZK,
                                              DISTRICT_CODE)
        school_rows2 = get_subject_sum_rows(item_config.AVG_RANK_ITEM, table_config.QA_ZK, SCHOOL_CODE)
        result += (district_rows2 + school_rows2)

    result.insert(0, first_row_config.AVG_RANK_OF_SUM_SUBJECT)
    return result


def school_avg_of_subject_sum_table(base_student, index):
    district_rows1 = get_subject_sum_rows(item_config.AVG_ITEM, table_config.QA, DISTRICT_CODE)
    school_rows1 = get_subject_sum_rows(item_config.AVG_ITEM, table_config.QA, SCHOOL_CODE)
    result = district_rows1 + school_rows1[index:index + 1]

    if base_student == report_config.SPECIAL:
        district_rows2 = get_subject_sum_rows(item_config.AVG_ITEM, table_config.QA_ZK,
                                              DISTRICT_CODE)
        school_rows2 = get_subject_sum_rows(item_config.AVG_ITEM, table_config.QA_ZK, SCHOOL_CODE)
        result += (district_rows2 + school_rows2[index:index + 1])

    result.insert(0, first_row_config.AVG_OF_SUBJECT_SUM)
    return result


def district_distribution_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))

    ids, names = get_distributions(subject_name)
    names.insert(0, '科目')
    datarows = get_district_subject_distribution_values(subject_name, ids, table_code)
    datarows[0].insert(0, subject_name)
    return [names] + datarows


def district_subject_std_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, table_code)
    return [school_names] + [xresult] + [yresult] + [num]


def school_subject_std_table(base_student, table_code, subject_name, index):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, table_code)
    return [get_std_names(index)] + [xresult] + [yresult] + [num]


def district_subject_box_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    return [school_names] + get_district_subject_box_values(subject_name, table_code)


def school_subject_box_table(base_student, table_code, subject_name, index):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    return [get_std_names(index)] + get_district_subject_box_values(subject_name, table_code)


def district_num_of_subject_table(base_student):
    district_rows1 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA, DISTRICT_CODE)
    school_rows1 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA, SCHOOL_CODE)
    result = district_rows1 + school_rows1

    if base_student == report_config.SPECIAL:
        district_rows2 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA_ZK,
                                          DISTRICT_CODE)
        school_rows2 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA_ZK, SCHOOL_CODE)
        result += (district_rows2 + school_rows2)

    result.insert(0, first_row_config.NUM_OF_SUBJECT)
    return result


def school_num_of_subject_table(base_student, index):
    district_rows1 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA, DISTRICT_CODE)
    school_rows1 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA, SCHOOL_CODE)
    result = district_rows1 + school_rows1[index:index + 1]

    if base_student == report_config.SPECIAL:
        district_rows2 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA_ZK,
                                          DISTRICT_CODE)
        school_rows2 = get_subject_rows(item_config.NUM_ITEM, base_student, table_config.QA_ZK, SCHOOL_CODE)
        result += (district_rows2 + school_rows2[index:index + 1])

    result.insert(0, first_row_config.NUM_OF_SUBJECT)
    return result


def district_sum_line_of_table(base_student):
    datarows = get_district_sum_line_of_rows(report_config.LINE_ITEMS_2, base_student)
    return [first_row_config.LINE_OF_25_60_85] + datarows


def school_sum_line_of_table(base_student, index):
    datarows = get_district_sum_line_of_rows(report_config.LINE_ITEMS_2, base_student)
    return [first_row_config.LINE_OF_25_60_85] + datarows[index:index + 1]


def district_dimen_avg_table(base_student, subject_id):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_avg_item = item_config.DIMEN_AVG_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        district_rows = get_subject_rows(dimen_avg_item, table_config.QA_ZK,
                                         DISTRICT_CODE, title_extra=False)
        school_rows = get_subject_rows(dimen_avg_item, table_config.QA_ZK, SCHOOL_CODE, title_extra=False)
    elif base_student == report_config.CURRENT:
        district_rows = get_subject_rows(dimen_avg_item, table_config.QA, DISTRICT_CODE, title_extra=False)
        school_rows = get_subject_rows(dimen_avg_item, table_config.QA, SCHOOL_CODE, title_extra=False)
    dimen_description.insert(0, "学校")
    return [dimen_description] + district_rows + school_rows


def district_avg_rank_of_sum_subject_of_class_table(base_student):
    if base_student == report_config.SPECIAL:
        sum_table = table_config.QA_ZK_CLASS_SUM_TABLE
        dimen_table = table_config.QA_ZK_CLASS_DIMEN_TABLE
    elif base_student == report_config.CURRENT:
        sum_table = table_config.QA_CLASS_SUM_TABLE
        dimen_table = table_config.QA_CLASS_DIMEN_TABLE

    item = item_config.AVG_RANK_ITEM
    ids, names = report_config.get_class_ids()
    class_sum_cell = qa.Cell(item, sum_table,
                             [[school_where, class_where], exam_where])
    class_subject_cell = qa.CellWithOrders(item, dimen_table,
                                           [[school_where, class_where], exam_where], "subjectId", subject_ids)
    class_sum_row = qa.ColSeriesCell(class_sum_cell, ids)
    class_subject_row = qa.ColSeriesCell(class_subject_cell, ids)

    datarows = qa.DataRows.combine_col_rows(class_sum_row, class_subject_row)
    return [first_row_config.AVG_RANK_OF_SUM_SUBJECT_CLASS] + list_util.combine_values_by_col(names, datarows)


if __name__ == '__main__':
    # print_rows(district_avg_rank_of_subject_sum_table(report_config.SPECIAL))
    # print_rows(district_avg_rank_of_subject_sum_table(report_config.CURRENT))
    #
    # print()
    #
    # print_rows(school_avg_of_subject_sum_table(report_config.SPECIAL, 0))
    # print_rows(school_avg_of_subject_sum_table(report_config.CURRENT, 0))
    #
    # print()
    #
    # print_rows(district_distribution_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_distribution_table(report_config.CURRENT, table_config.QA, "总分"))
    #
    # print()
    #
    # print_rows(district_subject_std_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_subject_std_table(report_config.CURRENT, table_config.QA, "总分"))
    #
    # print()
    #
    # print_rows(school_subject_std_table(report_config.SPECIAL, table_config.QA, "语文", 0))
    # print_rows(school_subject_std_table(report_config.CURRENT, table_config.QA, "总分", 0))
    #
    # print()
    #
    # print_rows(district_subject_box_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_subject_box_table(report_config.CURRENT, table_config.QA, "总分"))
    #
    # print()
    #
    # print_rows(school_subject_box_table(report_config.SPECIAL, table_config.QA, "语文", 0))
    # print_rows(school_subject_box_table(report_config.CURRENT, table_config.QA, "总分", 0))
    #
    # print()
    #
    # print_rows(district_num_of_subject_table(report_config.SPECIAL))
    # print_rows(district_num_of_subject_table(report_config.CURRENT))
    #
    # print()
    #
    # print_rows(school_num_of_subject_table(report_config.SPECIAL, 0))
    # print_rows(school_num_of_subject_table(report_config.CURRENT, 0))
    #
    # print()
    #
    # print_rows(district_sum_line_of_table(report_config.SPECIAL))
    # print_rows(district_sum_line_of_table(report_config.CURRENT))
    #
    # print()
    #
    # print_rows(school_sum_line_of_table(report_config.SPECIAL, 0))
    # print_rows(school_sum_line_of_table(report_config.CURRENT, 0))
    #
    # print()

    # print_rows(district_dimen_avg_table(report_config.SPECIAL, "语文"))
    # print_rows(district_dimen_avg_table(report_config.CURRENT, "语文"))

    print_rows(district_avg_rank_of_sum_subject_of_class_table(report_config.base_student))
