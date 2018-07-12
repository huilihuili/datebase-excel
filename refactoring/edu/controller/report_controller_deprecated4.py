import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.config.first_row_config as first_row_config
import refactoring.edu.config.report_config as report_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao

import numpy as np
import datetime

REAL_TABLE_EXTRA_TITLE = "(实考)"
JUNIOR_TABLE_EXTRA_TITLE = "(中考)"

REAL_CHART_EXTRA_TITLE = "实考",
JUNIOR_CHART_EXTRA_TITLE = "(参与中考)"

school_ids, school_names = report_config.get_school_info()
school_types = report_config.get_school_type()

district_ids, district_names = report_config.get_district_info()
subject_ids, subject_names = report_config.get_subject_info()

exam = report_config.exam
class_ids, class_names = report_config.get_class_ids()
grade_lev = report_config.exam.grade_lev
exam_id = report_config.exam.exam_id
exam_where = qa.Where("examId", exam_id)
district_where = qa.Where("districtId")
school_where = qa.Where("schoolId")
subject_where = qa.Where("subjectId")
class_where = qa.Where('classId')

district_len = len(district_ids)
school_len = len(school_ids)
class_len = len(class_ids)

all_exam_ids = qam_dao.get_exam_ids(exam)
all_exam_nicks = report_config.EXAM_NICKS_2

base_student = report_config.SPECIAL


def get_rank_diff_exam_ids(exam_ids):
    length = len(exam_ids)

    result = []
    for index in range(length - 1):
        result.append([exam_ids[index], exam_ids[index + 1]])
    if length > 2:
        result.append([exam_ids[0], exam_ids[- 1]])
    return result


def get_rank_diff_exam_nicks(exam_nicks):
    length = len(exam_nicks)

    result = []
    for index in range(length - 1):
        result.append("%s - %s" % (exam_nicks[index + 1], exam_nicks[index]))

    if length > 2:
        result.append("%s - %s" % (exam_nicks[0], exam_nicks[- 1]))
    return result


def get_class_index(school_id, class_id):
    for index in range(class_len):
        if school_id == class_ids[index][0] and class_id == class_ids[index][1]:
            return index


def get_school_index(school_id):
    for index in range(school_len):
        if school_ids[index] == school_id:
            return index


def get_district_index(district_id):
    for index in range(district_len):
        if district_ids[index] == district_id:
            return index


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


def get_district_subject_values(item, table_code):
    varied_where = district_where
    table = table_config.get_district_dimen_table(table_code)
    ids = district_ids

    subject_cell = qa.CellWithOrders(item, table, [varied_where, exam_where], "subjectId", subject_ids)
    subject_row = qa.ColSeriesCell(subject_cell, ids)
    return subject_row.get_values()


def get_school_subject_values(item, table_code):
    varied_where = school_where
    table = table_config.get_school_dimen_table(table_code)
    ids = school_ids

    subject_cell = qa.CellWithOrders(item, table, [varied_where, exam_where], "subjectId", subject_ids)
    subject_row = qa.ColSeriesCell(subject_cell, ids)
    return subject_row.get_values()


def get_district_exam_values(item, table_code, subject_id):
    subject_where.set_value(subject_id)
    varied_where = district_where
    table = table_config.get_district_dimen_table(table_code)
    ids = district_ids

    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_ids = all_exam_ids[start:end + 1]
    exam_cell = qa.CellWithOrders(item, table, [varied_where, subject_where], "examId", exam_ids)
    exam_row = qa.ColSeriesCell(exam_cell, ids)
    return exam_row.get_values()


def get_school_exam_values(item, table_code, subject_id):
    subject_where.set_value(subject_id)
    varied_where = school_where
    table = table_config.get_school_dimen_table(table_code)
    ids = school_ids

    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_ids = all_exam_ids[start:end + 1]
    exam_cell = qa.CellWithOrders(item, table, [varied_where, subject_where], "examId", exam_ids)
    exam_row = qa.ColSeriesCell(exam_cell, ids)
    return exam_row.get_values()


def get_exam_subject_values(item, table_code, school_id, subject_id):
    subject_where.set_value(subject_id)
    school_where.set_value(school_id)
    varied_where = exam_where
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_ids = all_exam_ids[start:end + 1]

    table = table_config.get_school_dimen_table(table_code)
    ids = exam_ids

    exam_cell = qa.Cell(item, table, [varied_where, school_where, subject_where])
    exam_row = qa.ColSeriesCell(exam_cell, ids)
    return exam_row.get_values()


def get_exam_rank_diff_values(item, table_code, school_id, subject_id):
    font_subject_where = qa.Where("font.subjectId", subject_id)
    behind_subject_where = qa.Where("behind.subjectId", subject_id)
    font_school_where = qa.Where("font.schoolId", school_id)
    behind_school_where = qa.Where("behind.schoolId", school_id)

    varied_where = [qa.Where("font.examId"), qa.Where("behind.examId")]
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_ids = all_exam_ids[start:end + 1]
    exam_diff_ids = get_rank_diff_exam_ids(exam_ids)

    table = table_config.get_school_dimen_table(table_code)
    table = ["%s AS font" % table, "%s AS behind" % table]
    ids = exam_diff_ids

    exam_cell = qa.Cell(item, table, [varied_where, font_school_where, behind_school_where, font_subject_where,
                                      behind_subject_where])
    exam_row = qa.ColSeriesCell(exam_cell, ids)
    return exam_row.get_values()


def get_district_sum_values(item, table_code):
    subject_values = get_district_subject_values(item, table_code)

    varied_where = district_where
    table = table_config.get_district_sum_table(table_code)
    ids = district_ids

    sum_cell = qa.Cell(item, table, [varied_where, exam_where])
    sum_row = qa.ColSeriesCell(sum_cell, ids)
    return list_util.combine_values_by_col(sum_row.get_values(), subject_values)


def get_school_sum_values(item, table_code):
    subject_values = get_school_subject_values(item, table_code)

    varied_where = school_where
    table = table_config.get_school_sum_table(table_code)
    ids = school_ids

    sum_cell = qa.Cell(item, table, [varied_where, exam_where])
    sum_row = qa.ColSeriesCell(sum_cell, ids)
    return list_util.combine_values_by_col(sum_row.get_values(), subject_values)


def get_class_sum_subject_avg_rank_values():
    if base_student == report_config.SPECIAL:
        sum_table = table_config.QA_ZK_CLASS_SUM_TABLE
        dimen_table = table_config.QA_ZK_CLASS_DIMEN_TABLE
    elif base_student == report_config.CURRENT:
        sum_table = table_config.QA_CLASS_SUM_TABLE
        dimen_table = table_config.QA_CLASS_DIMEN_TABLE

    item = item_config.AVG_RANK_ITEM

    class_sum_cell = qa.Cell(item, sum_table,
                             [[school_where, class_where], exam_where])
    class_subject_cell = qa.CellWithOrders(item, dimen_table,
                                           [[school_where, class_where], exam_where], "subjectId", subject_ids)
    class_sum_row = qa.ColSeriesCell(class_sum_cell, class_ids)
    class_subject_row = qa.ColSeriesCell(class_subject_cell, class_ids)

    return qa.DataRows.combine_col_rows(class_sum_row, class_subject_row)


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

    school_subject_avg_cell = qa.Cell("ROUND(avg / %d, 2)" % subject_total, school_table, wheres)
    school_subject_avg_row = qa.RowSeriesCell(school_subject_avg_cell, school_ids)

    stu_subject_sum_cell = qa.Cell("sum", stu_table, wheres)
    stu_subject_sum_row = qa.ColSeriesCell(stu_subject_sum_cell, school_ids)

    for value in stu_subject_sum_row.get_values():
        yresult.append(round(np.std(value, ddof=1), 2))
    xresult = school_subject_avg_row.get_values()[0]
    num = school_subject_num_row.get_values()[0]
    return xresult, yresult, num


def get_class_subject_items_values(item, table_code, subject_id):
    table = table_config.get_class_dimen_table(table_code)
    subject_where.set_value(subject_id)

    line_cell = qa.Cell(item, table, [[school_where, class_where], subject_where, exam_where])
    line_row = qa.ColSeriesCell(line_cell, class_ids)
    return line_row.get_values()


def get_district_subject_rows(item, table_code, first_col_exra=None):
    subject_values = get_district_subject_values(item, table_code)

    if first_col_exra is None:
        first_col = district_names
    else:
        first_col = list_util.add_something_to_list(first_col_exra, district_names)
    return list_util.combine_values_by_col(first_col, subject_values)


def get_school_subject_rows(item, table_code, first_col_exra=None):
    subject_values = get_school_subject_values(item, table_code)

    if first_col_exra is None:
        first_col = school_names
    else:
        first_col = list_util.add_something_to_list(first_col_exra, school_names)
    return list_util.combine_values_by_col(first_col, subject_values)


def get_district_sum_rows(item, table_code, first_col_exra=None):
    sum_values = get_district_sum_values(item, table_code)

    if first_col_exra is None:
        first_col = district_names
    else:
        first_col = list_util.add_something_to_list(first_col_exra, district_names)
    return list_util.combine_values_by_col(first_col, sum_values)


def get_school_sum_rows(item, table_code, first_col_exra=None):
    sum_values = get_school_sum_values(item, table_code)

    if first_col_exra is None:
        first_col = school_names
    else:
        first_col = list_util.add_something_to_list(first_col_exra, school_names)
    return list_util.combine_values_by_col(first_col, sum_values)


def get_district_sum_line_of_rows(item, table_code):
    if table_code == table_config.QA:
        table = table_config.QA_SCHOOL_LINE_TABLE
    elif table_code == table_config.QA_ZK:
        table = table_config.QA_ZK_SCHOOL_LINE_TABLE
    varied_where = school_where
    line_cell = qa.Cell(item, table, [varied_where, exam_where])
    line_row = qa.ColSeriesCell(line_cell, school_ids)
    return list_util.combine_values_by_col(school_names, line_row.get_values())


def get_district_subject_items_rows(item, table_code, subject_id):
    table = table_config.get_district_dimen_table(table_code)
    subject_where.set_value(subject_id)
    varied_where = district_where

    line_cell = qa.Cell(item, table, [varied_where, subject_where, exam_where])
    line_row = qa.ColSeriesCell(line_cell, district_ids)
    return list_util.combine_values_by_col(district_names, line_row.get_values())


def get_school_subject_items_rows(item, table_code, subject_id):
    table = table_config.get_school_dimen_table(table_code)
    subject_where.set_value(subject_id)
    varied_where = school_where

    line_cell = qa.Cell(item, table, [varied_where, subject_where, exam_where])
    line_row = qa.ColSeriesCell(line_cell, school_ids)
    return list_util.combine_values_by_col(school_names, line_row.get_values())


def print_rows(rows):
    for row in rows:
        print(row)


def district_subject_sum_table(base_student):
    district_item = item_config.AVG_NULL_ITEM
    school_item = item_config.AVG_RANK_ITEM
    first_row = first_row_config.AVG_RANK_OF_SUM_SUBJECT
    first_col_exra = None
    if base_student == report_config.SPECIAL:
        first_col_exra = REAL_TABLE_EXTRA_TITLE

    district_rows = get_district_sum_rows(district_item, table_config.QA,
                                          first_col_exra=first_col_exra)
    school_rows = get_school_sum_rows(school_item, table_config.QA, first_col_exra=first_col_exra)
    result = district_rows + school_rows

    if base_student == report_config.SPECIAL:
        if grade_lev == 2:
            first_col_exra = JUNIOR_TABLE_EXTRA_TITLE
        district_rows = get_district_sum_rows(district_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        school_rows = get_school_sum_rows(school_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        result += (district_rows + school_rows)
    result.insert(0, first_row)
    return result


def school_subject_sum_table(base_student, index):
    district_item = item_config.AVG_ITEM
    school_item = item_config.AVG_ITEM
    first_row = first_row_config.AVG_OF_SUM_SUBJECT

    first_col_exra = None
    if base_student == report_config.SPECIAL:
        first_col_exra = REAL_TABLE_EXTRA_TITLE

    district_rows = get_district_sum_rows(district_item, table_config.QA,
                                          first_col_exra=first_col_exra)
    school_rows = get_school_sum_rows(school_item, table_config.QA, first_col_exra=first_col_exra)
    result = district_rows + school_rows[index:index + 1]

    if base_student == report_config.SPECIAL:
        if grade_lev == 2:
            first_col_exra = JUNIOR_TABLE_EXTRA_TITLE
        district_rows = get_district_sum_rows(district_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        school_rows = get_school_sum_rows(school_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        result += (district_rows + school_rows[index:index + 1])
    result.insert(0, first_row)
    return result


def district_num_of_subject_table(base_student):
    district_item = item_config.NUM_ITEM
    school_item = item_config.NUM_ITEM
    first_row = first_row_config.NUM_OF_SUBJECT

    first_col_exra = None
    if base_student == report_config.SPECIAL:
        first_col_exra = REAL_TABLE_EXTRA_TITLE

    district_rows = get_district_subject_rows(district_item, table_config.QA,
                                              first_col_exra=first_col_exra)
    school_rows = get_school_subject_rows(school_item, table_config.QA, first_col_exra=first_col_exra)
    result = district_rows + school_rows

    if base_student == report_config.SPECIAL:
        if grade_lev == 2:
            first_col_exra = JUNIOR_TABLE_EXTRA_TITLE
        district_rows = get_district_subject_rows(district_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        school_rows = get_school_subject_rows(school_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        result += (district_rows + school_rows)
    result.insert(0, first_row)
    return result


def school_num_of_subject_table(base_student, index):
    district_item = item_config.NUM_ITEM
    school_item = item_config.NUM_ITEM
    first_row = first_row_config.NUM_OF_SUBJECT

    first_col_exra = None
    if base_student == report_config.SPECIAL:
        first_col_exra = REAL_TABLE_EXTRA_TITLE

    district_rows = get_district_sum_rows(district_item, table_config.QA,
                                          first_col_exra=first_col_exra)
    school_rows = get_school_sum_rows(school_item, table_config.QA, first_col_exra=first_col_exra)
    result = district_rows + school_rows[index:index + 1]

    if base_student == report_config.SPECIAL:
        if grade_lev == 2:
            first_col_exra = JUNIOR_TABLE_EXTRA_TITLE
        district_rows = get_district_sum_rows(district_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        school_rows = get_school_sum_rows(school_item, table_config.QA_ZK, first_col_exra=first_col_exra)
        result += (district_rows + school_rows[index:index + 1])
    result.insert(0, first_row)
    return result


def district_sum_line_of_table(base_student):
    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    result = get_district_sum_line_of_rows(report_config.LINE_ITEMS_2, table_code)
    result.insert(0, first_row_config.LINE_OF_25_60_85)
    return result


def school_sum_line_of_table(base_student, index):
    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    result = get_district_sum_line_of_rows(report_config.LINE_ITEMS_2, table_code)[index:index + 1]
    result.insert(0, first_row_config.LINE_OF_25_60_85)
    return result


def district_dimen_avg_table(base_student, subject_id):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_avg_item = item_config.DIMEN_AVG_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    district_rows = get_district_subject_rows(dimen_avg_item, table_code, subject_id)
    school_rows = get_school_subject_rows(dimen_avg_item, table_code, subject_id)
    result = district_rows + school_rows
    dimen_description.insert(0, "学校")
    result.insert(0, dimen_description)
    return result


def district_avg_rank_of_sum_subject_of_class_table():
    valus = get_class_sum_subject_avg_rank_values()
    result = list_util.combine_values_by_col(class_names, valus)
    result.insert(0, first_row_config.AVG_RANK_OF_SUM_SUBJECT_CLASS)
    return result


def school_dimen_ratio_table(subject_id, index):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_avg_item = item_config.DIMEN_RATIO_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    district_rows = get_district_subject_rows(dimen_avg_item, table_code, subject_id)
    school_rows = get_school_subject_rows(dimen_avg_item, table_code, subject_id)
    result = [district_rows[0], district_rows[district_ids.index(school_types[index])], school_rows[index]]
    dimen_description.insert(0, "学校")
    result.insert(0, dimen_description)
    return result


def class_avg_rank_of_sum_subject_table(school_id, class_id):
    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    item = item_config.AVG_ITEM
    district_values = get_district_sum_values(item, table_code)
    school_rows = get_school_sum_values(item, table_code)

    class_values = get_class_sum_subject_avg_rank_values()
    index = get_class_index(school_id, class_id)
    class_rank = ['排名'] + class_values[index][1::2]
    class_avg = ['班级平均分'] + class_values[index][::2]
    school_avg = ['学校平均分'] + school_rows[get_school_index(school_id)]
    district_avg = ['区平均分'] + district_values[0]
    result = [class_rank, class_avg, district_avg, school_avg]
    return result


def class_dimen_ratio_table(school_id, class_id, subject_id):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_item = item_config.DIMEN_RATIO_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    district_rows = get_district_subject_items_rows(dimen_item, table_code, subject_id)
    school_rows = get_school_subject_items_rows(dimen_item, table_code, subject_id)
    class_values = get_class_subject_items_values(dimen_item, table_code, subject_id)

    class_row = ['班级'] + class_values[get_class_index(school_id, class_id)]
    school_row = school_rows[get_school_index(school_id)]
    district_row = district_rows[0]
    result = [class_row, school_row, district_row]
    dimen_description.insert(0, "知识块（类别）")
    result.insert(0, dimen_description)
    return result


def school_avg_rank_table(subject_id, index):
    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    item = item_config.AVG_ITEM
    district_avg_values = get_district_exam_values(item, table_code, subject_id)
    school_avg_values = get_school_exam_values(item, table_code, subject_id)
    item = item_config.RANK_ITEM
    school_rank_values = get_school_exam_values(item, table_code, subject_id)

    district_avg_row = ['区平均分'] + district_avg_values[0]
    similar_avg_row = ['同类学校平均分'] + district_avg_values[get_district_index(school_types[index])]
    school_avg_row = ['校平均分'] + school_avg_values[index]
    school_rank_row = ['排名'] + school_rank_values[index]
    result = [school_rank_row, school_avg_row, similar_avg_row, district_avg_row]

    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_nicks = all_exam_nicks[start:end + 1]
    exam_nicks.insert(0, "考试(类别)")

    result.insert(0, exam_nicks)
    return result


def school_exam_dimen_rank_table(subject_id, index):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_item = item_config.DIMEN_RANK_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    school_values = get_exam_subject_values(dimen_item, table_code, school_ids[index], subject_id)
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_nicks = all_exam_nicks[start:end + 1]
    result = list_util.combine_values_by_col(exam_nicks, school_values)
    dimen_description.insert(0, "知识块(排名)")
    result.insert(0, dimen_description)
    return result


def school_exam_dimen_avg_table(subject_id, index):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_item = item_config.DIMEN_AVG_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    school_values = get_exam_subject_values(dimen_item, table_code, school_ids[index], subject_id)
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_nicks = all_exam_nicks[start:end + 1]
    result = list_util.combine_values_by_col(exam_nicks, school_values)
    dimen_description.insert(0, "知识块(平均分)")
    result.insert(0, dimen_description)
    return result


def school_exam_dimen_rank_diff_table(subject_id, index):
    subject_where.set_value(subject_id)
    dimen_description = qam_dao.get_dimen_description_by_exam(exam_where, subject_where)
    dimen_length = len(dimen_description)
    dimen_item = item_config.DIMEN_RANK_DIFF_ITEMS[0:dimen_length]

    if base_student == report_config.SPECIAL:
        table_code = table_config.QA_ZK
    elif base_student == report_config.CURRENT:
        table_code = table_config.QA

    school_values = get_exam_rank_diff_values(dimen_item, table_code, school_ids[index], subject_id)
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    exam_nicks = all_exam_nicks[start:end + 1]
    exam_diff_nicks = get_rank_diff_exam_nicks(exam_nicks)
    result = list_util.combine_values_by_col(exam_diff_nicks, school_values)
    dimen_description.insert(0, "知识块(排名)")
    result.insert(0, dimen_description)
    return result


def district_distribution_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))

    ids, names = get_distributions(subject_name)
    names.insert(0, '科目')
    datarows = get_district_subject_distribution_values(subject_name, ids, table_code)
    datarows[0].insert(0, subject_name)
    return [names] + datarows


def district_std_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, table_code)
    return [school_names] + [xresult] + [yresult] + [num]


def school_std_table(base_student, table_code, subject_name, index):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    xresult, yresult, num = get_district_subject_std_values(subject_name, table_code)
    return [get_std_names(index)] + [xresult] + [yresult] + [num]


def district_box_table(base_student, table_code, subject_name):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    return [school_names] + get_district_subject_box_values(subject_name, table_code)


def school_box_table(base_student, table_code, subject_name, index):
    if base_student == report_config.SPECIAL:
        print(report_config.get_chart_extra_title(table_code))
    return [get_std_names(index)] + get_district_subject_box_values(subject_name, table_code)


if __name__ == '__main__':
    d1 = datetime.datetime.now()

    school_id = "002F2A5004B9421EBEC2AAD8A6CEB044"
    class_id = "0A036FDF66274D31B8DEC6F7E07A820F"
    subject_id = 121
    index = 0

    # print_rows(district_subject_sum_table(report_config.SPECIAL))
    # print_rows(school_subject_sum_table(report_config.SPECIAL, 0))
    #
    # print_rows(district_num_of_subject_table(report_config.SPECIAL))
    # print_rows(school_num_of_subject_table(report_config.SPECIAL, 0))
    #
    # print_rows(district_sum_line_of_table(report_config.SPECIAL))
    # print_rows(school_sum_line_of_table(report_config.SPECIAL, 0))
    #
    # print_rows(district_dimen_avg_table(report_config.SPECIAL, 121))
    #
    # print_rows(school_dimen_ratio_table(121, 0))
    #
    # print_rows(district_avg_rank_of_sum_subject_of_class_table())

    # print_rows(class_avg_rank_of_sum_subject_table(school_id, class_id))
    #
    # print_rows(class_dimen_ratio_table(school_id, class_id, subject_id))
    #
    # print_rows(school_avg_rank_table(subject_id, index))
    #
    # print_rows(school_exam_dimen_rank_table(subject_id, index))
    #
    # print_rows(school_exam_dimen_rank_diff_table(subject_id, index))
    #
    # print_rows(school_exam_dimen_avg_table(subject_id, index))
    #
    # print_rows(district_distribution_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_distribution_table(report_config.SPECIAL, table_config.QA, "总分"))
    #
    print_rows(district_std_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_std_table(report_config.SPECIAL, table_config.QA, "总分"))
    #
    # print_rows(school_std_table(report_config.SPECIAL, table_config.QA, "语文", 0))
    # print_rows(school_std_table(report_config.SPECIAL, table_config.QA, "总分", 0))
    #
    # print_rows(district_box_table(report_config.SPECIAL, table_config.QA, "语文"))
    # print_rows(district_box_table(report_config.SPECIAL, table_config.QA, "总分"))
    #
    # print_rows(school_box_table(report_config.SPECIAL, table_config.QA, "语文", 0))
    # print_rows(school_box_table(report_config.SPECIAL, table_config.QA, "总分", 0))

    d2 = datetime.datetime.now()
    print()
    print(d2 - d1)
