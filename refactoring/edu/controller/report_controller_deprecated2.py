import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.config.first_row_config as first_row_config
import refactoring.edu.config.report_config as report_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa

import numpy as np

school_ids, school_names = report_config.get_school_info()
district_ids, district_names = report_config.get_district_info()
subject_ids, subject_names = report_config.get_subject_info()

exam_id = report_config.exam.exam_id
exam_where = qa.Where("examId", exam_id)
district_where = qa.Where("districtId")
school_where = qa.Where("schoolId")
subject_where = qa.Where("subjectId")

DISTRICT_CODE = 1
SCHOOL_CODE = 2

district_len = len(district_ids)
school_len = len(school_ids)


def get_names(type_code, district_code):
    if type_code == report_config.SPECIAL:
        current_extra_title = report_config.get_table_extra_title(table_config.QA)
        special_extra_title = report_config.get_table_extra_title(table_config.QA_ZK)
        if district_code == DISTRICT_CODE:
            district_names_with_current = list_util.add_something_to_list(
                current_extra_title, district_names)
            district_names_with_special = list_util.add_something_to_list(special_extra_title, district_names)
            return district_names_with_current + district_names_with_special
        elif district_code == SCHOOL_CODE:
            school_names_with_current = list_util.add_something_to_list(current_extra_title, school_names)
            school_names_with_special = list_util.add_something_to_list(special_extra_title, school_names)
            return school_names_with_current + school_names_with_special
    elif type_code == report_config.CURRENT:
        if district_code == DISTRICT_CODE:
            return district_names
        elif district_code == SCHOOL_CODE:
            return school_names


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


def get_subject_sum_values(item, type_code, district_code):
    if district_code == DISTRICT_CODE:
        dimen_table, sum_table = table_config.get_district_table(type_code)
        varied_where = district_where
        ids = district_ids
    elif district_code == SCHOOL_CODE:
        dimen_table, sum_table = table_config.get_school_table(type_code)
        varied_where = school_where
        ids = school_ids

    subject_cell = qa.CellWithOrders(item, dimen_table, [varied_where, exam_where], "subjectId", subject_ids)
    subject_row = qa.ColSeriesCell(subject_cell, ids)

    sum_cell = qa.Cell(item, sum_table, [varied_where, exam_where])
    sum_row = qa.ColSeriesCell(sum_cell, ids)
    return list_util.combine_values_by_col(sum_row.get_values(), subject_row.get_values())


def get_subject_sum_rows(item, type_code, district_code):
    qa_values = get_subject_sum_values(item, table_config.QA, district_code)
    names = get_names(type_code, district_code)
    if type_code == report_config.SPECIAL:
        qa_zk_values = get_subject_sum_values(item, table_config.QA_ZK, district_code)
        return list_util.combine_values_by_col(names, qa_values + qa_zk_values)
    elif type_code == report_config.CURRENT:
        return list_util.combine_values_by_col(names, qa_values)


def get_school_template(district_rows, type_code, title):
    result = district_rows
    if type_code == report_config.SPECIAL:
        result.insert(district_len, [])
    result.append([])
    result.insert(0, title)
    return result


def get_school_subject_sum_avg_rows_template(item, type_code):
    district_subject_sum_avg_rows = get_subject_sum_rows(item, type_code, DISTRICT_CODE)
    return get_school_template(district_subject_sum_avg_rows, type_code, first_row_config.AVG_OF_SUM_SUBJECT)


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


def get_district_subject_std_values(subject_name, type_code, table_code):
    wheres = [school_where, exam_where]
    if subject_name == "总分":
        stu_table = table_config.get_stu_sum_table(table_code)
        school_table = table_config.get_school_table(type_code)[1]
    else:
        stu_table = table_config.get_stu_dimen_table(table_code)
        school_table = table_config.get_school_table(type_code)[0]

        subject_where.set_value(get_subject_id_by_name(subject_name))
        wheres.append(subject_where)

    subject_total = report_config.get_total(subject_name)

    xresult = []
    yresult = []

    school_subject_num_cell = qa.Cell("num_nz", school_table, wheres)
    school_subject_num_row = qa.RowSeriesCell(school_subject_num_cell, school_ids)
    for school_id in school_ids:
        school_where.set_value(school_id)
        school_subject_avg_cell = qa.Cell("avg", school_table, wheres)
        stu_subject_sum_cell = qa.Cell("sum", stu_table, wheres)
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


school_subject_sum_avg_rows = get_subject_sum_rows(item_config.AVG_ITEM, report_config.base_student, SCHOOL_CODE)
school_subject_sum_avg_rows_template = get_school_subject_sum_avg_rows_template(item_config.AVG_ITEM,
                                                                                report_config.base_student)


def district_table(district_rows, school_rows, base_student):
    if base_student == report_config.CURRENT:
        result = district_rows + school_rows
    elif base_student == report_config.SPECIAL:
        result = district_rows[0:district_len] + \
                 school_rows[0:school_len] + \
                 district_rows[district_len:] + \
                 school_rows[school_len:]
    return result


def district_subject_sum_table():
    district_subject_sum_rows = get_subject_sum_rows(item_config.AVG_NULL_ITEM, report_config.base_student,
                                                     DISTRICT_CODE)
    school_subject_sum_rows = get_subject_sum_rows(item_config.AVG_RANK_ITEM, report_config.base_student, SCHOOL_CODE)
    result = district_table(district_subject_sum_rows, school_subject_sum_rows, report_config.base_student)
    result.insert(0, first_row_config.AVG_RANK_OF_SUM_SUBJECT)
    return result


def school_subject_sum_table(index):
    if report_config.base_student == report_config.CURRENT:
        school_subject_sum_avg_rows_template[-1] = school_subject_sum_avg_rows[index]
    elif report_config.base_student == report_config.SPECIAL:
        school_subject_sum_avg_rows_template[district_len + 1] = school_subject_sum_avg_rows[0:school_len][index]
        school_subject_sum_avg_rows_template[-1] = school_subject_sum_avg_rows[school_len:][index]
    return school_subject_sum_avg_rows_template


def get_district_subject_distribution_table(subject_name, table_code):
    type_code = report_config.base_student
    if type_code == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))

    ids, names = get_distributions(subject_name)
    names.insert(0, '科目')
    datarows = get_district_subject_distribution_values(subject_name, ids, table_code)
    datarows[0].insert(0, subject_name)
    return [names] + datarows


def get_district_subject_std_table(subject_name, table_code):
    type_code = report_config.base_student
    if type_code == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, type_code, table_code)
    return [school_names] + [xresult] + [yresult] + [num]


def get_school_subject_std_table(subject_name, table_code, index):
    type_code = report_config.base_student
    if type_code == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, type_code, table_code)
    return [get_std_names(index)] + [xresult] + [yresult] + [num]


def get_district_subject_box_table(subject_name, table_code):
    return [school_names] + get_district_subject_box_values(subject_name, table_code)


def get_school_subject_box_table(subject_name, table_code, index):
    return [get_std_names(index)] + get_district_subject_box_values(subject_name, table_code)


if __name__ == '__main__':
    print_rows(district_subject_sum_table())

    print()

    print_rows(school_subject_sum_table(0))

    print()

    print_rows(get_district_subject_distribution_table("语文", table_config.QA))
    print_rows(get_district_subject_distribution_table("总分", table_config.QA_ZK))

    print()

    print_rows(get_district_subject_std_table("语文", table_config.QA))
    print_rows(get_district_subject_std_table("总分", table_config.QA_ZK))
    print_rows(get_school_subject_std_table("总分", table_config.QA_ZK, 0))

    print()
    print_rows(get_district_subject_box_table("语文", table_config.QA))
    print_rows(get_district_subject_box_table("总分", table_config.QA_ZK))
    print_rows(get_school_subject_box_table("总分", table_config.QA_ZK, 0))

    print()
