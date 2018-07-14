import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao
import refactoring.edu.config.first_row_config as first_row_config
import refactoring.edu.entrance.handler as handler
import datetime
import numpy as np
import refactoring.edu.util.plt_util as plt_util
import refactoring.edu.util.excel_util as excel_util
import os
import threading


def createDir(path):
    if os.path.exists(path):
        print(" “" + path + '” 已经存在')
    else:
        print("创建名为 “" + path + '” 的文件夹...')
        os.makedirs(path)


DISTRICT_CODE = 1
SCHOOL_CODE = 2
CLASS_CODE = 3
STU_CODE = 4

QA_CODE = 1
QA_ZK_CODE = 2
QAT_CODE = 3

SUBJECT_CODE = 1
SUM_CODE = 2


def get_subject_code(subject_id):
    if subject_id is None:
        return SUM_CODE
    else:
        return SUBJECT_CODE


def print_rows(rows):
    for row in rows:
        print(row)


def box(titles, school_stu, names, path):
    plt_util.boxplot(titles, school_stu, lables=names, path=path)


def scatter(titles, x_value, y_value, names, lines, point_size, path):
    plt_util.scatter(titles, x_value, y_value, texts=names, xDif=- 0.001,
                     yDif=0.1, lines=lines, points=point_size, path=path)


class Value(object):
    def __init__(self, exam, gradation, where):
        self.exam = exam
        self.gradation = gradation
        self.where = where

        # self.exam = handler.Exam()
        # self.gradation = handler.Gradation()
        # self.where = handler.Where()

        self.cell_where = qa.CellWhere()
        self.cell_order = qa.CellOrder()

        self.cell = qa.Cell(where_list=self.cell_where)
        self.order_cell = qa.CellWithOrders(where_list=self.cell_where, order=self.cell_order)

        self.row_value = qa.RowSeriesCell()
        self.col_value = qa.ColSeriesCell()

    def set_varied_district(self, district_code):
        self.cell_where.varied = self.where.get_varied_district(district_code)

    def set_exam_subject_order(self, item, table_code, district_code):
        self.order_cell.select_name = item
        self.order_cell.table_name = table_config.get_subject_score_table_name(table_code, district_code)
        self.set_varied_district(district_code)
        self.col_value.set(self.order_cell, self.exam.get_district_varied_ids(district_code))

    def get_exam_subject(self, item, table_code, district_code):
        self.set_exam_subject_order(item, table_code, district_code)
        self.cell_where.fixed = self.where.get_fixed_exam()
        self.cell_order.set("subjectId", self.exam.gradation.subject_ids)
        return self.col_value.get_values()

    def get_subject_exam(self, item, table_code, district_code, subject_id):
        self.set_exam_subject_order(item, table_code, district_code)
        self.cell_where.fixed = self.where.get_fixed_subject(subject_id)
        self.cell_order.set("examId", self.exam.get_subject_exam_ids(subject_id))
        return self.col_value.get_values()

    def set_one_row(self, item, table_code, district_code, subject_id=None):
        self.cell.select_name = item
        self.cell.table_name = table_config.get_score_table_name(table_code, district_code,
                                                                 get_subject_code(subject_id))
        self.cell_where.fixed = self.where.get_fixed_exam_subject(subject_id)

    def get_district_one_row(self, item, table_code, district_code, subject_id=None):
        self.set_one_row(item, table_code, district_code, subject_id)
        self.set_varied_district(district_code)
        self.row_value.set(self.cell, self.exam.get_district_varied_ids(district_code))
        return self.row_value.get_values()

    def get_score_distribution(self, item, table_code, subject_id=None):
        self.set_one_row(item, table_code, STU_CODE, subject_id)
        self.cell_where.varied = self.where.get_varied_greater_less_equal()
        self.row_value.set(self.cell, self.exam.get_subject_distribution_ids(subject_id))
        return self.row_value.get_values()

    def get_all_distribution(self, item, table_code, subject_id=None):
        ids = self.exam.get_subject_distribution_ids(subject_id)
        self.set_one_row(item, table_code, STU_CODE, subject_id)
        self.cell_where.varied = self.where.get_varied_greater_equal_less_equal()
        self.row_value.set(self.cell, ids[0:1])
        greater_equal_value = self.row_value.get_values()

        self.cell_where.varied = self.where.get_varied_greater_less_equal()
        self.row_value.set(self.cell, ids[1:])
        greater_value = self.row_value.get_values()
        return list_util.to_a_list([greater_equal_value, greater_value])

    def get_count_distribution(self, item, table_code):
        self.set_one_row(item, table_code, STU_CODE, None)
        self.cell_where.varied = self.where.get_varied_greater_less_equal()
        self.cell_where.fixed = self.where.get_exam_count_fixed_where(self.exam.count)
        self.row_value.set(self.cell, self.exam.get_subject_distribution_ids(None))
        return self.row_value.get_values()

    def get_subject_distribution(self, item, table_code, subject_id=None):
        distribution_type = self.exam.get_subject_distribution_type(subject_id)
        if distribution_type == handler.Distribution.ALL:
            return self.get_all_distribution(item, table_code, subject_id)
        elif distribution_type == handler.Distribution.SCORE:
            return self.get_score_distribution(item, table_code, subject_id)
        elif distribution_type == handler.Distribution.COUNT:
            return self.get_score_distribution(item, table_code)

    def set_exam_district_subject(self, item, district_code, subject_id):
        self.cell.select_name = item
        self.cell_where.varied = self.where.get_varied_district(district_code)
        self.cell_where.fixed = self.where.get_fixed_exam_subject(subject_id)
        self.col_value.set(self.cell, self.exam.get_district_varied_ids(district_code))

    def get_school_stu(self, item, table_code, subject_id=None):
        self.set_exam_district_subject(item, SCHOOL_CODE, subject_id)
        self.cell.table_name = table_config.get_stu_score_table(table_code, get_subject_code(subject_id))
        return self.col_value.get_values()

    def get_exam_dimen(self, item, table_code, district_code, subject_id):
        self.set_exam_district_subject(item, district_code, subject_id)
        self.cell.table_name = table_config.get_subject_score_table_name(table_code, district_code)
        return self.col_value.get_values()

    def get_exam_school_line(self, item, table_code):
        self.set_exam_district_subject(item, SCHOOL_CODE, None)
        self.cell.table_name = table_config.get_school_sum_line(table_code)
        return self.col_value.get_values()

    def get_subject_dimen(self, item, table_code, district_code, id, subject_id):
        self.cell.select_name = item
        self.cell.table_name = table_config.get_subject_score_table_name(table_code, district_code)
        self.cell_where.fixed = self.where.get_fixed_district_subject(district_code, id, subject_id)
        self.cell_where.varied = self.where.get_varied_exam()
        self.col_value.set(self.cell, self.exam.get_subject_exam_ids(subject_id))
        return self.col_value.get_values()

    def get_dimen_diff(self, item, table_code, school_id, subject_id):
        self.cell.select_name = item
        self.cell.table_name = table_config.get_school_rank_diff_table(table_code)
        self.cell_where.fixed = self.where.get_fixed_diff_school_subject(school_id, subject_id)
        self.cell_where.varied = self.where.get_varied_exam_diff()
        self.col_value.set(self.cell, self.exam.get_subject_exam_diff_ids(subject_id))
        return self.col_value.get_values()


class Table(object):
    def __init__(self, value):
        self.value = value
        # self.value = Value()

        self.exam = value.exam
        self.gradation = value.gradation

        self.base_student = self.exam.base_student

        self.exam_subject_dimen_description = []
        self.exam_diff_subject_dimen_desctiption = []
        for subject_id in value.gradation.subject_ids:
            self.exam_subject_dimen_description.append(
                qam_dao.get_dimen_description_by_exam(self.exam.exam_id, subject_id))
            self.exam_diff_subject_dimen_desctiption.append(
                qam_dao.get_dimen_description_by_exams(self.exam.get_exam_ids(subject_id), subject_id))

    def get_subject_title(self, table_code, function, subject_id=None):
        if table_code == QA_CODE:
            extra = first_row_config.REAL_CHART_EXTRA_TITLE
        elif table_code == QA_ZK_CODE:
            if self.gradation.grade_lev == 2:
                extra = first_row_config.JUNIOR_CHART_EXTRA_TITLE

        if subject_id is None:
            title = "区%s总分%s" % (extra, function)
        else:
            title = "区%s%s%s" % (extra, self.gradation.get_subject_name_by_id(subject_id), function)
        return title

    def get_subject_distribution(self, table_code, subject_id=None):
        title = self.get_subject_title(table_code, "分数分布", subject_id)
        item = item_config.COUNT_ITEM
        print(title)
        print(["分数段"] + self.exam.get_subject_distribution_names())
        print(["人数"] + self.value.get_subject_distribution(item, table_code))

    def get_distribution(self, table_code):
        self.get_subject_distribution(table_code)
        for subject_id in self.gradation.subject_ids:
            self.get_subject_distribution(table_code, subject_id)

    def get_all_distribution(self):
        self.get_distribution(QA_CODE)
        if self.base_student == self.exam.SPECIAL:
            self.get_distribution(QA_ZK_CODE)

    def get_district_first_col(self, table_code):
        district_names = self.gradation.district_names
        school_names = self.exam.school_names
        if self.exam.base_student == handler.Exam.SPECIAL:
            if table_code == QA_ZK_CODE:
                extra = first_row_config.JUNIOR_TABLE_EXTRA_TITLE
            elif table_code == QA_CODE:
                extra = first_row_config.REAL_TABLE_EXTRA_TITLE
            district_names = list_util.add_something_to_list(extra, district_names)
            school_names = list_util.add_something_to_list(extra, school_names)
        first_col = district_names + school_names
        return first_col

    def get_school_first_col(self, school_id, table_code):
        district_names = self.gradation.district_names
        school_names = self.exam.school_names
        if self.exam.base_student == handler.Exam.SPECIAL:
            if table_code == QA_ZK_CODE:
                extra = first_row_config.JUNIOR_TABLE_EXTRA_TITLE
            elif table_code == QA_CODE:
                extra = first_row_config.REAL_TABLE_EXTRA_TITLE
            district_names = list_util.add_something_to_list(extra, district_names)
            school_names = list_util.add_something_to_list(extra, school_names)
        school_index = self.exam.get_school_index(school_id)
        first_col = district_names + school_names[school_index:school_index + 1]
        return first_col

    def get_district_school_avg_rank(self, table_code):
        first_col = self.get_district_first_col(table_code)

        item = item_config.AVG_ITEM
        district_sum_avg = self.value.get_district_one_row(item, table_code, DISTRICT_CODE)
        school_sum_avg = self.value.get_district_one_row(item, table_code, SCHOOL_CODE)
        district_subject_avg = self.value.get_exam_subject(item, table_code, DISTRICT_CODE)
        school_subject_avg = self.value.get_exam_subject(item, table_code, SCHOOL_CODE)

        item = item_config.RANK_ITEM
        school_subject_rank = self.value.get_exam_subject(item, table_code, SCHOOL_CODE)
        school_sum_rank = self.value.get_district_one_row(item, table_code, SCHOOL_CODE)
        subject_len = len(self.gradation.subject_names)
        district_len = len(self.gradation.district_names)
        district_subject_avg_rank = list_util.cross_several_row(district_subject_avg,
                                                                [[''] * subject_len] * district_len)
        school_subject_avg_rank = list_util.cross_several_row(school_subject_avg, school_subject_rank)
        district_value = list_util.combine_values_by_col(district_sum_avg, [''] * subject_len,
                                                         district_subject_avg_rank, )
        school_value = list_util.combine_values_by_col(school_sum_avg, school_sum_rank, school_subject_avg_rank)
        print_rows(list_util.combine_values_by_col(first_col, district_value + school_value))

    def get_all_district_school_avg_rank(self):
        first_row = first_row_config.AVG_RANK_OF_SUM_SUBJECT
        print(first_row)
        self.get_district_school_avg_rank(QA_CODE)
        if self.exam.base_student == handler.Exam.SPECIAL:
            self.get_district_school_avg_rank(QA_ZK_CODE)

    def get_school_avg_rank(self, table_code, school_id):
        first_col = self.get_school_first_col(school_id, table_code)

        item = item_config.AVG_ITEM
        district_sum_avg = self.value.get_district_one_row(item, table_code, DISTRICT_CODE)
        school_sum_avg = self.value.get_district_one_row(item, table_code, SCHOOL_CODE)
        district_subject_avg = self.value.get_exam_subject(item, table_code, DISTRICT_CODE)
        school_subject_avg = self.value.get_exam_subject(item, table_code, SCHOOL_CODE)

        district_value = list_util.combine_values_by_col(district_sum_avg, district_subject_avg)
        school_value = list_util.combine_values_by_col(school_sum_avg, school_subject_avg)
        school_index = self.exam.get_school_index(school_id)
        print_rows(
            list_util.combine_values_by_col(first_col, district_value + school_value[school_index:school_index + 1]))

    def get_all_school_avg_rank(self, school_id):
        first_row = first_row_config.AVG_OF_SUM_SUBJECT
        print(first_row)
        self.get_school_avg_rank(QA_CODE, school_id)
        if self.exam.base_student == handler.Exam.SPECIAL:
            self.get_school_avg_rank(QA_ZK_CODE, school_id)

    def get_district_num(self, table_code):
        first_col = self.get_district_first_col(table_code)
        item = item_config.NUM_ITEM
        district_subject_num = self.value.get_exam_subject(item, table_code, DISTRICT_CODE)
        school_subject_num = self.value.get_exam_subject(item, table_code, SCHOOL_CODE)
        print_rows(list_util.combine_values_by_col(first_col, district_subject_num + school_subject_num))

    def get_all_district_num(self):
        first_row = first_row_config.NUM_OF_SUBJECT
        print(first_row)
        self.get_district_num(QA_CODE)
        if self.exam.base_student == handler.Exam.SPECIAL:
            self.get_district_num(QA_ZK_CODE)

    def get_school_num(self, table_code, school_id):
        first_col = self.get_school_first_col(school_id, table_code)
        item = item_config.NUM_ITEM
        district_subject_num = self.value.get_exam_subject(item, table_code, DISTRICT_CODE)
        school_subject_num = self.value.get_exam_subject(item, table_code, SCHOOL_CODE)
        school_index = self.exam.get_school_index(school_id)
        print_rows(list_util.combine_values_by_col(first_col, district_subject_num + school_subject_num[
                                                                                     school_index:school_index + 1]))

    def get_all_school_num(self, school_id):
        first_row = first_row_config.NUM_OF_SUBJECT
        print(first_row)
        self.get_school_num(QA_CODE, school_id)
        if self.exam.base_student == handler.Exam.SPECIAL:
            self.get_school_num(QA_ZK_CODE, school_id)

    def get_all_district_line(self):
        first_row = first_row_config.LINE_OF_25_60_85
        print(first_row)
        table_code = QA_CODE
        if self.exam.base_student == handler.Exam.SPECIAL:
            table_code = QA_ZK_CODE

        first_col = self.exam.school_names
        item = item_config.LINE_25_60_85_ITEMS
        school_sum_line = self.value.get_exam_school_line(item, table_code)
        print_rows(list_util.combine_values_by_col(first_col, school_sum_line))

    def get_all_school_line(self, school_id):
        first_row = first_row_config.LINE_OF_25_60_85
        print(first_row)
        table_code = QA_CODE
        if self.exam.base_student == handler.Exam.SPECIAL:
            table_code = QA_ZK_CODE

        item = item_config.LINE_25_60_85_ITEMS
        school_sum_line = self.value.get_exam_school_line(item, table_code)
        index = self.exam.get_school_index(school_id)
        first_col = self.exam.school_names
        print_rows(list_util.combine_values_by_col(first_col[index:index + 1], school_sum_line[index:index + 1]))

    def get_all_district_dimen_avg(self, subject_id):
        index = self.gradation.get_subject_index(subject_id)
        first_row = self.exam_subject_dimen_description[index]
        dimen_len = len(first_row)
        first_row.insert(0, "学校")
        print(first_row)
        table_code = QA_CODE
        if self.exam.base_student == handler.Exam.SPECIAL:
            table_code = QA_ZK_CODE

        first_col = self.exam.school_names + self.gradation.district_names
        item = item_config.DIMEN_AVG_ITEMS[:dimen_len]
        district_dimen_avg = self.value.get_exam_dimen(item, table_code, DISTRICT_CODE, subject_id)
        school_dimen_avg = self.value.get_exam_dimen(item, table_code, SCHOOL_CODE, subject_id)
        print_rows(list_util.combine_values_by_col(first_col, district_dimen_avg + school_dimen_avg))

    def get_all_district_class_avg_rank(self):
        first_row = first_row_config.AVG_RANK_OF_SUM_SUBJECT_CLASS
        print(first_row)
        table_code = QA_CODE
        if self.exam.base_student == handler.Exam.SPECIAL:
            table_code = QA_ZK_CODE

        first_col = self.exam.class_names
        item = item_config.AVG_ITEM
        class_subject_avg = self.value.get_exam_subject(item, table_code, CLASS_CODE)
        class_sum_avg = self.value.get_district_one_row(item, table_code, CLASS_CODE)

        item = item_config.RANK_ITEM
        class_subject_rank = self.value.get_exam_subject(item, table_code, CLASS_CODE)
        class_sum_rank = self.value.get_district_one_row(item, table_code, CLASS_CODE)
        class_sum = list_util.combine_values_by_col(class_sum_avg, class_sum_rank)
        class_subject = list_util.cross_several_row(class_subject_avg, class_subject_rank)
        print_rows(list_util.combine_values_by_col(first_col, class_sum, class_subject))


class Pic(object):
    def __init__(self, value):
        self.value = value
        self.exam = value.exam
        self.gradation = value.gradation
        self.base_student = self.exam.base_student
        self.names = [self.exam.school_names]
        for school_id in self.exam.school_ids:
            self.names.append(self.exam.get_std_school_names(school_id))

    def get_subject_title(self, table_code, function, subject_id=None):
        if table_code == QA_CODE:
            extra = first_row_config.REAL_CHART_EXTRA_TITLE
        elif table_code == QA_ZK_CODE:
            if self.gradation.grade_lev == 2:
                extra = first_row_config.JUNIOR_CHART_EXTRA_TITLE
        if subject_id is None:
            title = "区%s总分%s" % (extra, function)
        else:
            title = "区%s%s%s" % (extra, self.gradation.get_subject_name_by_id(subject_id), function)
        return title

    def get_subject_std(self, table_code, subject_id=None):
        item = item_config.AVG_RATIO_ITEM % self.exam.get_subject_total(subject_id)
        x_values = self.value.get_district_one_row(item, table_code, SCHOOL_CODE)

        item = item_config.NUM_ITEM
        point_size = self.value.get_district_one_row(item, table_code, SCHOOL_CODE)

        item = item_config.SUM_ITEM
        school_stu = self.value.get_school_stu(item, table_code, subject_id)

        y_values = []
        for value in school_stu:
            y_values.append(round(np.std(value, ddof=1), 2))
        title = self.get_subject_title(table_code, "箱形图", subject_id)
        titles = [title, "学校", "分数"]

        directory = r"E:\reportData\junior\区"
        path = r"%s\%s.png" % (directory, title)
        box(titles, school_stu, self.names[0], path)

        for index, name in enumerate(self.names[1:]):
            directory = r"E:\reportData\junior\%s" % name[index]
            path = r"%s\%s.png" % (directory, title)
            box(titles, school_stu, name, path)

        title = self.get_subject_title(table_code, "标准差-平均分得分率二维图", subject_id)
        titles = [title, "平均得分率", "标准差"]
        lines = [['vline', (max(x_values) + min(x_values)) / 2],
                 ['hline', (max(y_values) + min(y_values)) / 2]]
        directory = r"E:\reportData\junior\区"
        path = r"%s\%s.png" % (directory, title)
        scatter(titles, x_values, y_values, self.names[0], lines, point_size, path)
        plt_util.scatter(titles, x_values, y_values, texts=self.names[0], lines=lines, xDif=- 0.001,
                         yDif=0.1, points=point_size,
                         path=r"%s\%s.png" % (directory, title))
        for index, name in enumerate(self.names[1:]):
            directory = r"E:\reportData\junior\%s" % name[index]
            path = r"%s\%s.png" % (directory, title)
            scatter(titles, x_values, y_values, name, lines, point_size, path)

    def get_std(self, table_code):
        self.get_subject_std(table_code)
        for subject_id in self.gradation.subject_ids:
            self.get_subject_std(table_code, subject_id)

    def get_all_std(self):
        directory = r"E:\reportData\junior\区"
        createDir(directory)
        for index, name in enumerate(self.names[1:]):
            directory = r"E:\reportData\junior\%s" % name[index]
            createDir(directory)
        self.get_std(QA_CODE)
        if self.base_student == self.exam.SPECIAL:
            self.get_std(QA_ZK_CODE)


def value_test():
    d1 = datetime.datetime.now()

    subject_id = 121

    enroll_year = 2014
    grade_lev = 2
    gradation = handler.Gradation(enroll_year, grade_lev)

    exam_id = '8c4646637f44489c9ba9333e580fe9d0'
    base_student = handler.Exam.SPECIAL
    exam = handler.Exam(gradation, exam_id, base_student)

    school_id = exam.get_school_ids()[0]
    where = handler.Where(exam.exam_id)

    value = Value(exam, gradation, where)
    print(value.get_exam_subject(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE))
    print()
    print(value.get_subject_exam(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE, subject_id))
    print()
    print(value.get_district_one_row(item_config.AVG_RATIO_ITEM % 150, QA_CODE, SCHOOL_CODE, subject_id))
    print()
    print(value.get_district_one_row(item_config.AVG_ITEM, QA_ZK_CODE, DISTRICT_CODE))
    print()
    print(value.get_district_one_row(item_config.AVG_ITEM, QA_ZK_CODE, SCHOOL_CODE))
    print()
    print(value.get_district_one_row(item_config.AVG_ITEM, QA_ZK_CODE, CLASS_CODE))
    print()
    print(value.get_score_distribution(item_config.COUNT_ITEM, QA_ZK_CODE))
    print()
    print(value.get_all_distribution(item_config.COUNT_ITEM, QA_ZK_CODE))
    print()
    print(value.get_count_distribution(item_config.COUNT_ITEM, QA_ZK_CODE))
    print()
    print(value.get_school_stu(item_config.SUM_ITEM, QA_ZK_CODE))
    print()
    print(value.get_school_stu(item_config.SUM_ITEM, QA_ZK_CODE, subject_id=subject_id))
    print()
    print(value.get_exam_dimen(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, SCHOOL_CODE, subject_id))
    print()
    print(value.get_exam_school_line(item_config.LINE_25_60_85_ITEMS, QA_ZK_CODE))
    print()
    print(value.get_subject_dimen(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, SCHOOL_CODE,
                                  school_id, subject_id))
    print()
    print(value.get_dimen_diff(item_config.DIMEN_RANK_DIFF_ITEMS[0:8], QA_ZK_CODE, school_id,
                               subject_id))
    print()
    d2 = datetime.datetime.now()
    print(d2 - d1)


def table_test():
    d1 = datetime.datetime.now()
    enroll_year = 2014
    grade_lev = 2
    gradation = handler.Gradation(enroll_year, grade_lev)

    exam_id = '8c4646637f44489c9ba9333e580fe9d0'
    base_student = handler.Exam.SPECIAL
    exam = handler.Exam(gradation, exam_id, base_student)
    where = handler.Where(exam.exam_id)
    value = Value(exam, gradation, where)

    # table = Table(value)
    # school_id = exam.school_ids[0]
    # subject_id = gradation.subject_ids[0]
    # table.get_all_distribution()
    # table.get_all_district_school_avg_rank()
    # table.get_all_school_avg_rank(school_id)
    # table.get_all_district_num()
    # table.get_all_school_num(school_id)
    # table.get_all_district_line()
    # table.get_all_school_line(school_id)
    # table.get_all_district_dimen_avg(subject_id)
    # table.get_all_district_class_avg_rank()
    pic = Pic(value)
    pic.get_all_std()
    d2 = datetime.datetime.now()
    print(d2 - d1)


if __name__ == '__main__':
    table_test()
