import numpy as np
import datetime

import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao
import refactoring.edu.util.list_util as list_util

exam_id = "8c4646637f44489c9ba9333e580fe9d0"
exam_where = qa.Where('examId', '8c4646637f44489c9ba9333e580fe9d0')
subject_where = qa.Where("subjectId", 121)
district_where = qa.Where('districtId', "9")
school_where = qa.Where('schoolId', "002F2A5004B9421EBEC2AAD8A6CEB044")
class_where = qa.Where('classId', "0A036FDF66274D31B8DEC6F7E07A820F")
font_exam_where = qa.Where("font.examId")
behind_exam_where = qa.Where("behind.examId")
font_school_where = qa.Where("font.schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
behind_school_where = qa.Where("behind.schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
font_subject_where = qa.Where("font.subjectId", 121)
behind_subject_where = qa.Where("behind.subjectId", 121)

grade_lev = 2

null_item = "''"
num_item = "num_nz"
subject_item = "subjectId"
subject_avg_item = 'round(avg, 2)'
subject_rank_item = 'rank'
exam_item = "examId"
subject_avg_null_item = [subject_avg_item, null_item]
subject_avg_rank_item = [subject_avg_item, subject_rank_item]
line_items = ["line25", "line60", "line85"]
dimen_avg_items = ["round(dimen1Avg, 2)", "round(dimen2Avg, 2)", "round(dimen3Avg, 2)", "round(dimen4Avg, 2)",
                   "round(dimen5Avg, 2)", "round(dimen6Avg, 2)", "round(dimen7Avg, 2)", "round(dimen8Avg, 2)"]

dimen_ratio_items = ["round(dimen1Ratio, 2)", "round(dimen2Ratio, 2)", "round(dimen3Ratio, 2)", "round(dimen4Ratio, 2)",
                     "round(dimen5Ratio, 2)", "round(dimen6Ratio, 2)",
                     "round(dimen7Ratio, 2)", "round(dimen8Ratio, 2)"]

dimen_rank_diff_items = ["font.dimen1Rank - behind.dimen1Rank",
                         "font.dimen2Rank - behind.dimen2Rank",
                         "font.dimen3Rank - behind.dimen3Rank",
                         "font.dimen4Rank - behind.dimen4Rank",
                         "font.dimen5Rank - behind.dimen5Rank",
                         "font.dimen6Rank - behind.dimen6Rank",
                         "font.dimen7Rank - behind.dimen7Rank",
                         "font.dimen8Rank - behind.dimen8Rank", ]

sum_avg_five_item = "round(avg_five, 2)"
sum_rank_five_item = "rank_five"
sum_avg_null_item = [sum_avg_five_item, null_item]
sum_avg_rank_item = [sum_avg_five_item, sum_rank_five_item]

district_dimen_table = "qa_district_dimen"
district_sum_table = "qa_district_sum"
school_dimen_table = "qa_school_dimen"
school_sum_table = "qa_school_sum"
stu_dimen_table = "qa_stu_dimen"
school_line_table = "qa_school_line"
class_dimen_table = "qa_class_dimen"
class_sum_table = "qa_class_sum"
school_rank_diff_table = ["qa_school_dimen AS font", "qa_school_dimen AS behind"]
district_ids = qam_dao.get_all_district_ids()
district_names = qam_dao.get_all_district_names()
school_ids = qam_dao.get_all_school_ids(grade_lev)
school_names = qam_dao.get_all_school_names(grade_lev)
school_class_ids = qam_dao.get_all_school_class_ids(class_sum_table, exam_id, grade_lev, sum_rank_five_item)
school_class_names = qam_dao.get_all_school_class_names(class_sum_table, exam_id, grade_lev,
                                                        sum_rank_five_item)
district_school_names = list_util.to_a_list([district_names, school_names])
subject_ids = [121, 122, 103, 118, 128]
exam_ids = ["3f2a81437b944569aacb675a6544b2f3", "7c5315bb7c7a4cdb854d2893bfaebce5", "661cb10d97ae48c4a7207f1da9f6acdd",
            "8c4646637f44489c9ba9333e580fe9d0", "af8535da67de463ea7e5617168157ad4"]

exam_diff_ids = [["3f2a81437b944569aacb675a6544b2f3", "7c5315bb7c7a4cdb854d2893bfaebce5"],
                 ["7c5315bb7c7a4cdb854d2893bfaebce5", "661cb10d97ae48c4a7207f1da9f6acdd"],
                 ["661cb10d97ae48c4a7207f1da9f6acdd", "8c4646637f44489c9ba9333e580fe9d0"],
                 ["8c4646637f44489c9ba9333e580fe9d0", "af8535da67de463ea7e5617168157ad4"],
                 ["3f2a81437b944569aacb675a6544b2f3", "af8535da67de463ea7e5617168157ad4"]]

subject_names = ['语文', '数学', '英语', '物理', '化学']
exam_names = ["初中预备", "初一期末", "初二期末", "初三一模", "初三二模"]

exam_diff_names = ["初一期末-初中预备", "初二期末-初一期末",
                   "初三一模-初二期末", "初三二模-初三一模", "初三二模-初中预备"]

line_names = ["前25人数", "前60人数", "前85人数"]
dimen_names = ["dimen1Avg", "dimen2Avg", "dimen3Avg", "dimen4Avg", "dimen5Avg", "dimen6Avg", "dimen7Avg", "dimen8Avg"]


def test1():
    district_subject_cell = qa.CellWithOrders(subject_avg_item, district_dimen_table,
                                              [district_where, exam_where], subject_item, subject_ids)

    district_subject_row = qa.ColSeriesCell(district_subject_cell, district_ids)

    district_sum_cell = qa.Cell(sum_avg_five_item, district_sum_table,
                                [district_where, exam_where])

    district_sum_row = qa.ColSeriesCell(district_sum_cell, district_ids)

    datarows = qa.DataRows.combine_col_rows(district_sum_row, district_subject_row)
    for table_row in list_util.combine_values_by_col(district_names, datarows):
        print(table_row)


def test2():
    school_subject_cell = qa.CellWithOrders(subject_avg_item, school_dimen_table,
                                            [school_where, exam_where], subject_item, subject_ids)
    school_subject_row = qa.ColSeriesCell(school_subject_cell, school_ids)

    school_sum_cell = qa.Cell(sum_avg_five_item, school_sum_table,
                              [school_where, exam_where])
    school_sum_row = qa.ColSeriesCell(school_sum_cell, school_ids)

    datarows = qa.DataRows.combine_col_rows(school_sum_row, school_subject_row)
    for table_row in list_util.combine_values_by_col(school_names, datarows):
        print(table_row)


def test3():
    district_subject_cell = qa.CellWithOrders(num_item, district_dimen_table,
                                              [district_where, exam_where], subject_item, subject_ids)

    district_subject_row = qa.ColSeriesCell(district_subject_cell, district_ids)

    datarows = district_subject_row.get_values()
    for table_row in list_util.combine_values_by_col(district_names, datarows):
        print(table_row)


def test4():
    school_subject_cell = qa.CellWithOrders(num_item, school_dimen_table,
                                            [school_where, exam_where], subject_item, subject_ids)
    school_subject_row = qa.ColSeriesCell(school_subject_cell, school_ids)

    datarows = school_subject_row.get_values()
    for table_row in list_util.combine_values_by_col(school_names, datarows):
        print(table_row)


def test5():
    school_dimen_ratio_cell = qa.Cell(dimen_ratio_items, school_dimen_table,
                                      [school_where, exam_where, subject_where])
    school_dimen_ratio_row = qa.ColSeriesCell(school_dimen_ratio_cell, school_ids)

    datarows = school_dimen_ratio_row.get_values()
    for table_row in list_util.combine_values_by_col(school_names, datarows):
        print(table_row)


def test6():
    district_exams_avg_cell = qa.CellWithOrders(subject_avg_item, district_dimen_table,
                                                [district_where, subject_where], exam_item, exam_ids)
    district_exams_avg_row = qa.ColSeriesCell(district_exams_avg_cell, district_ids)

    datarows = district_exams_avg_row.get_values()
    for table_row in list_util.combine_values_by_col(district_names, datarows):
        print(table_row)


def test7():
    school_exams_avg_cell = qa.CellWithOrders(subject_avg_item, school_dimen_table,
                                              [school_where, subject_where], exam_item, exam_ids)
    school_exams_avg_row = qa.ColSeriesCell(school_exams_avg_cell, school_ids)

    datarows = school_exams_avg_row.get_values()
    for table_row in list_util.combine_values_by_col(school_names, datarows):
        print(table_row)


def test8():
    school_rank_diff_cell = qa.Cell(dimen_avg_items, school_dimen_table,
                                    [exam_where, school_where, subject_where])
    school_rank_diff_row = qa.ColSeriesCell(school_rank_diff_cell, exam_ids)

    datarows = school_rank_diff_row.get_values()
    for table_row in list_util.combine_values_by_col(exam_names, datarows):
        print(table_row)


def test9():
    school_rank_diff_cell = qa.Cell(dimen_rank_diff_items, school_rank_diff_table,
                                    [[font_exam_where, behind_exam_where], font_school_where, behind_school_where,
                                     font_subject_where, behind_subject_where])
    school_rank_diff_row = qa.ColSeriesCell(school_rank_diff_cell, exam_diff_ids)

    datarows = school_rank_diff_row.get_values()
    for table_row in list_util.combine_values_by_col(exam_diff_names, datarows):
        print(table_row)


if __name__ == '__main__':
    d1 = datetime.datetime.now()
    test1()
    print()

    test2()
    print()

    test3()
    print()

    test4()
    print()

    test5()
    print()

    test6()
    print()

    test7()
    print()

    test8()
    print()

    test9()
    print()

    d2 = datetime.datetime.now()
    print(d2 - d1)
