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


grade_lev = 2

null_item = "''"
num_item = "num_nz"
subject_item = "subjectId"
subject_avg_item = 'round(avg, 2)'
subject_rank_item = 'rank'
subject_avg_null_item = [subject_avg_item, null_item]
subject_avg_rank_item = [subject_avg_item, subject_rank_item]
line_items = ["line25", "line60", "line85"]
dimen_avg_items = ["round(dimen1Avg, 2)", "round(dimen2Avg, 2)", "round(dimen3Avg, 2)", "round(dimen4Avg, 2)",
                   "round(dimen5Avg, 2)", "round(dimen6Avg, 2)", "round(dimen7Avg, 2)", "round(dimen8Avg, 2)"]

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

district_ids = qam_dao.get_all_district_ids()
district_names = qam_dao.get_all_district_names()
school_ids = qam_dao.get_all_school_ids(grade_lev)
school_names = qam_dao.get_all_school_names(grade_lev)
school_class_ids = qam_dao.get_all_school_class_ids(class_sum_table, exam_id, grade_lev, sum_rank_five_item)
school_class_names = qam_dao.get_all_school_class_names(class_sum_table, exam_id, grade_lev,
                                                        sum_rank_five_item)
district_school_names = list_util.to_a_list([district_names, school_names])
subject_ids = [121, 122, 103, 118, 128]
subject_names = ['语文', '数学', '英语', '物理', '化学']
line_names = ["前25人数", "前60人数", "前85人数"]
dimen_names = ["dimen1Avg", "dimen2Avg", "dimen3Avg", "dimen4Avg", "dimen5Avg", "dimen6Avg", "dimen7Avg", "dimen8Avg"]


def test1():
    district_subject_cell = qa.CellWithOrders(subject_avg_null_item, district_dimen_table,
                                              [district_where, exam_where], subject_item, subject_ids)

    district_subject_row = qa.ColSeriesCell(district_subject_cell, district_ids)

    district_sum_cell = qa.Cell(sum_avg_null_item, district_sum_table,
                                [district_where, exam_where])

    district_sum_row = qa.ColSeriesCell(district_sum_cell, district_ids)

    school_subject_cell = qa.CellWithOrders(subject_avg_rank_item, school_dimen_table,
                                            [school_where, exam_where], subject_item, subject_ids)
    school_subject_row = qa.ColSeriesCell(school_subject_cell, school_ids)

    school_sum_cell = qa.Cell(sum_avg_rank_item, school_sum_table,
                              [school_where, exam_where])
    school_sum_row = qa.ColSeriesCell(school_sum_cell, school_ids)

    first_row = ['类别', '语文', '排名', '数学', '英语', '排名', '物理', '排名', '化学', '排名', '总分', '排名']
    datarows = [[district_subject_row, district_sum_row], [school_subject_row, school_sum_row]]
    table_rows = qa.TableRows(first_row, district_school_names, *datarows)
    for table_row in table_rows.get_values():
        print(table_row)


def test2():
    ids = []
    names = []
    start, end, step = [0, 150, 5]
    scopes = range(start, end, step)

    for index, scope in enumerate(scopes[0:-1]):
        ids.append([scope, scopes[index + 1]])
        names.append("(%d, %d]" % (scope, scopes[index + 1]))
    if scopes[-1] < end:
        ids.append([scopes[-1], end])
        names.append("(%d, %d]" % (scopes[-1], end))
    names[0] = "[%d, %d]" % (scopes[0], scopes[1])

    greater_equal_where = qa.Where("sum", symbol=">=")
    greater_where = qa.Where("sum", symbol=">")
    less_equal_where = qa.Where("sum", symbol="<=")

    cell1 = qa.Cell("COUNT(*)", stu_dimen_table, [[greater_equal_where, less_equal_where], exam_where, subject_where])
    cell2 = qa.Cell("COUNT(*)", stu_dimen_table, [[greater_where, less_equal_where], exam_where, subject_where])
    row1 = qa.RowSeriesCell(cell1, ids[0:1])
    row2 = qa.RowSeriesCell(cell2, ids[1:])
    table = qa.TableRows(["分数段", names], ['个数'], [row1, row2])
    for table_row in table.get_values():
        print(table_row)


def test3():
    print(school_names)
    subject_total = 150
    xresult = []
    yresult = []
    school_subject_num_cell = qa.Cell("num_nz", "qa_school_dimen", [school_where, exam_where, subject_where])
    school_subject_num_row = qa.RowSeriesCell(school_subject_num_cell, school_ids)
    for school_id in school_ids:
        school_subject_avg_cell = qa.Cell("avg", "qa_school_dimen", [school_where, exam_where, subject_where])
        school_where.value = school_id
        xresult.append(school_subject_avg_cell.get_value() / subject_total)
        stu_subject_sum_cell = qa.Cell("sum", "qa_stu_dimen", [exam_where, school_where, subject_where])
        yresult.append(np.std(stu_subject_sum_cell.get_row_values(), ddof=1))
    print(xresult)
    print(yresult)
    print(school_subject_num_row.get_values()[0])


def test4():
    stu_subject_sum_cell = qa.Cell("sum", "qa_stu_dimen", [school_where, exam_where, subject_where])
    stu_subject_sum_row = qa.ColSeriesCell(stu_subject_sum_cell, school_ids)
    print(school_names)
    print(stu_subject_sum_row.get_values())


def test5():
    district_subject_cell = qa.CellWithOrders(num_item, district_dimen_table,
                                              [district_where, exam_where], subject_item, subject_ids)

    district_subject_row = qa.ColSeriesCell(district_subject_cell, district_ids)

    school_subject_cell = qa.CellWithOrders(num_item, school_dimen_table,
                                            [school_where, exam_where], subject_item, subject_ids)
    school_subject_row = qa.ColSeriesCell(school_subject_cell, school_ids)

    first_row = ['类别', '语文', '数学', '英语', '物理', '化学']
    datarows = [district_subject_row, school_subject_row]
    table_rows = qa.TableRows(first_row, district_school_names, *datarows)
    for table_row in table_rows.get_values():
        print(table_row)


def test6():
    school_sum_line_cell = qa.Cell(line_items, school_line_table,
                                   [school_where, exam_where])
    school_sum_line_row = qa.ColSeriesCell(school_sum_line_cell, school_ids)

    first_row = ['学校', line_names]
    datarows = school_sum_line_row
    table_rows = qa.TableRows(first_row, school_names, datarows)
    for table_row in table_rows.get_values():
        print(table_row)


def test7():
    district_dimen_avg_cell = qa.Cell(dimen_avg_items, district_dimen_table,
                                      [district_where, exam_where, subject_where])
    district_dimen_avg_row = qa.ColSeriesCell(district_dimen_avg_cell, district_ids)

    school_dimen_avg_cell = qa.Cell(dimen_avg_items, school_dimen_table,
                                    [school_where, exam_where, subject_where])
    school_dimen_avg_row = qa.ColSeriesCell(school_dimen_avg_cell, school_ids)

    first_row = ['学校', dimen_names]
    datarows = [district_dimen_avg_row, school_dimen_avg_row]
    table_rows = qa.TableRows(first_row, district_school_names, *datarows)
    for table_row in table_rows.get_values():
        print(table_row)


def test8_1():
    class_sum_avg_rank_cell = qa.Cell(sum_avg_rank_item, class_sum_table, [[school_where, class_where], exam_where])
    class_subject_avg_rank_cell = qa.CellWithOrders(subject_avg_rank_item, class_dimen_table,
                                                    [[school_where, class_where], exam_where], "subjectId", subject_ids)
    class_sum_avg_rank_row = qa.ColSeriesCell(class_sum_avg_rank_cell, school_class_ids)
    class_subject_rank_row = qa.ColSeriesCell(class_subject_avg_rank_cell, school_class_ids)
    first_row = ['学校', '班级', '总分', '排名', '语文', '排名', '数学', '英语', '排名', '物理', '排名', '化学', '排名', ]
    datarows = [class_sum_avg_rank_row, class_subject_rank_row]
    table_rows = qa.TableRows(first_row, school_class_names, datarows)
    for table_row in table_rows.get_values():
        print(table_row)


def test8_2():
    class_sum_avg_rank_cell = qa.Cell(sum_avg_rank_item, class_sum_table, [[school_where, class_where], exam_where])
    class_subject_avg_rank_cell = qa.Cell(subject_avg_rank_item, class_dimen_table,
                                          [[school_where, class_where], subject_where, exam_where])
    class_sum_avg_rank_row = qa.ColSeriesCell(class_sum_avg_rank_cell, school_class_ids)
    class_subject_rank_row = qa.BlockSeriesCell(class_subject_avg_rank_cell, school_class_ids, subject_ids)
    first_row = ['学校', '班级', '总分', '排名', '语文', '排名', '数学', '英语', '排名', '物理', '排名', '化学', '排名', ]
    datarows = [class_sum_avg_rank_row, class_subject_rank_row]
    table_rows = qa.TableRows(first_row, school_class_names, datarows)
    for table_row in table_rows.get_values():
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

    test8_1()
    print()

    d2 = datetime.datetime.now()
    print(d2 - d1)
