import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.config.first_row_config as first_row_config
import refactoring.edu.config.report_config as report_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao

import numpy as np
import datetime

QA_DISTRICT_DIMEN_TABLE = "qa_district_dimen"
QA_DISTRICT_SUM_TABLE = "qa_district_sum"
QA_SCHOOL_DIMEN_TABLE = "qa_school_dimen"
QA_SCHOOL_SUM_TABLE = "qa_school_sum"
QA_CLASS_DIMEN_TABLE = "qa_class_dimen"
QA_CLASS_SUM_TABLE = "qa_class_sum"
QA_STU_DIMEN_TABLE = "qa_stu_dimen"
QA_STU_SUM_TABLE = "qa_stu_sum"

QA_ZK_DISTRICT_DIMEN_TABLE = "qa_zk_district_dimen"
QA_ZK_DISTRICT_SUM_TABLE = "qa_zk_district_sum"
QA_ZK_SCHOOL_DIMEN_TABLE = "qa_zk_school_dimen"
QA_ZK_SCHOOL_SUM_TABLE = "qa_zk_school_sum"
QA_ZK_CLASS_DIMEN_TABLE = "qa_zk_class_dimen"
QA_ZK_CLASS_SUM_TABLE = "qa_zk_class_sum"
QA_ZK_STU_DIMEN_TABLE = "qa_zk_stu_dimen"
QA_ZK_STU_SUM_TABLE = "qa_zk_stu_sum"

QA_SCHOOL_LINE_TABLE = "qa_school_line"
QA_ZK_SCHOOL_LINE_TABLE = "qa_zk_school_line"

QAT_SCHOOL_DIMEN_TABLE = "qat_school_dimen"
QAT_DISTRICT_DIMEN_TABLE = "qat_district_dimen"

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
district_where = qa.Where("districtId", 9)
school_where = qa.Where("schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
subject_where = qa.Where("subjectId", 121)
class_where = qa.Where('classId', "0A036FDF66274D31B8DEC6F7E07A820F")

greater_where = qa.Where("sum", symbol=">")
less_equal_where = qa.Where("sum", symbol="<=")
greater_equal_where = qa.Where("sum", symbol=">=")
count_where = qa.Where("count")

district_len = len(district_ids)
school_len = len(school_ids)
class_len = len(class_ids)

all_exam_ids = qam_dao.get_exam_ids(exam)
all_exam_nicks = report_config.EXAM_NICKS_2

base_student = report_config.SPECIAL

DISTRICT_CODE = 1
SCHOOL_CODE = 2
CLASS_CODE = 3
STU_CODE = 4

QA_CODE = 1
QA_ZK_CODE = 2
QAT_CODE = 3

SUBJECT_CODE = 1
SUM_CODE = 2

SCORE_CODE = 1
LINE_CODE = 2


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


def get_subject_score_table_name(table_code, district_code):
    if district_code == DISTRICT_CODE:
        if table_code == QA_CODE:
            return QA_DISTRICT_DIMEN_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_DISTRICT_DIMEN_TABLE
        elif table_code == QAT_CODE:
            return QAT_DISTRICT_DIMEN_TABLE
    elif district_code == SCHOOL_CODE:
        if table_code == QA_CODE:
            return QA_SCHOOL_DIMEN_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_SCHOOL_DIMEN_TABLE
        elif table_code == QAT_CODE:
            return QAT_SCHOOL_DIMEN_TABLE
    elif district_code == CLASS_CODE:
        if table_code == QA_CODE:
            return QA_CLASS_DIMEN_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_CLASS_DIMEN_TABLE
    elif district_code == STU_CODE:
        if table_code == QA_CODE:
            return QA_STU_DIMEN_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_STU_DIMEN_TABLE


def get_sum_score_table_name(table_code, district_code):
    if district_code == DISTRICT_CODE:
        if table_code == QA_CODE:
            return QA_DISTRICT_SUM_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_DISTRICT_SUM_TABLE
    elif district_code == SCHOOL_CODE:
        if table_code == QA_CODE:
            return QA_SCHOOL_SUM_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_SCHOOL_SUM_TABLE
    elif district_code == CLASS_CODE:
        if table_code == QA_CODE:
            return QA_CLASS_SUM_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_CLASS_SUM_TABLE
    elif district_code == STU_CODE:
        if table_code == QA_CODE:
            return QA_STU_SUM_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_ZK_STU_SUM_TABLE


def get_sum_line_table_name(table_code, district_code):
    if district_code == SCHOOL_CODE:
        if table_code == QA_CODE:
            return QA_SCHOOL_LINE_TABLE
        elif table_code == QA_ZK_CODE:
            return QA_SCHOOL_LINE_TABLE


def get_score_table_name(table_code, district_code, subject_code):
    if subject_code == SUBJECT_CODE:
        return get_subject_score_table_name(table_code, district_code)
    elif subject_code == SUM_CODE:
        return get_sum_score_table_name(table_code, district_code)


def get_line_table_name(table_code, district_code, subject_code):
    if subject_code == SUM_CODE:
        return get_sum_line_table_name(table_code, district_code)


def get_table_name(table_code, district_code, subject_code, score_code):
    if score_code == SCORE_CODE:
        return get_score_table_name(table_code, district_code, subject_code)
    elif score_code == LINE_CODE:
        return get_line_table_name(table_code, district_code, subject_code)


def get_subject_exam_ids(subject_id):
    start, end = qam_dao.get_subject_exam_start_end(exam, subject_id)
    return all_exam_ids[start:end + 1]


def get_subject_code(subject_id):
    if subject_id is None:
        return SUM_CODE
    else:
        return SUBJECT_CODE


def get_district_varied_ids(district_code):
    if district_code == DISTRICT_CODE:
        return district_ids
    elif district_code == SCHOOL_CODE:
        return school_ids
    elif district_code == CLASS_CODE:
        return class_ids


class CellSelect(object):
    def __init__(self, item, table):
        self.item = item
        self.table = table

    @staticmethod
    def get_subject_select(item, table_code, district_code, subject_code):
        table = get_score_table_name(table_code, district_code, subject_code)
        return CellSelect(item, table)


class CellWhere(object):
    def __init__(self, varied, fixed):
        self.varied = varied
        self.fixed = fixed

    def get_where_list(self):
        where_list = [self.varied]
        if isinstance(self.fixed, list):
            where_list += self.fixed
        else:
            where_list.append(self.fixed)
        return where_list

    @staticmethod
    def get_subject_fixed_where(subject_id=None):
        fixed_where = [exam_where]
        if subject_id is not None:
            subject_where.set_value(subject_id)
            fixed_where.append(subject_where)
        return fixed_where

    @staticmethod
    def get_district_varied_where(district_code):
        if district_code == DISTRICT_CODE:
            return district_where
        elif district_code == SCHOOL_CODE:
            return school_where
        elif district_code == CLASS_CODE:
            return [school_where, class_where]


class CellOrder(object):
    def __init__(self, item, ids):
        self.item = item
        self.ids = ids


class CellFactory(object):
    @staticmethod
    def get_cell(select, where):
        return qa.Cell(select.item, select.table, where.get_where_list())

    @staticmethod
    def get_cell_with_order(select, where, order):
        return qa.CellWithOrders(select.item, select.table, where.get_where_list(),
                                 order.item, order.ids)


class ValueFactory(object):
    @staticmethod
    def get_row_value(cell, ids):
        return qa.RowSeriesCell(cell, ids).get_values()

    @staticmethod
    def get_col_value(cell, ids):
        return qa.ColSeriesCell(cell, ids).get_values()


class OrderValue(object):
    def __init__(self, item, district_code, table_code):
        self.select = CellSelect.get_subject_select(item, table_code, district_code, SUBJECT_CODE)
        self.varied_where = CellWhere.get_district_varied_where(district_code)
        self.varied_ids = get_district_varied_ids(district_code)

    def get_subject_value(self):
        where = CellWhere(self.varied_where, exam_where)
        order = CellOrder("subjectId", subject_ids)
        cell = CellFactory.get_cell_with_order(self.select, where, order)
        return ValueFactory.get_col_value(cell, self.varied_ids)

    def get_exam_value(self, subject_id):
        subject_where.set_value(subject_id)
        where = CellWhere(self.varied_where, subject_where)
        order = CellOrder("examId", get_subject_exam_ids(subject_id))
        cell = CellFactory.get_cell_with_order(self.select, where, order)
        return ValueFactory.get_col_value(cell, self.varied_ids)


class OneRowValue(object):
    def __init__(self, item, table_code, district_code, subject_id=None):
        self.select = CellSelect.get_subject_select(item, table_code, district_code, get_subject_code(subject_id))
        self.varied_where = CellWhere.get_district_varied_where(district_code)
        self.fixed_where = CellWhere.get_subject_fixed_where(subject_id)
        self.ids = get_district_varied_ids(district_code)

    def get_value(self):
        where = CellWhere(self.varied_where, self.fixed_where)
        cell = CellFactory.get_cell(self.select, where)
        return ValueFactory.get_row_value(cell, self.ids)[0]


class ScoreDistributionValue(object):
    def __init__(self, item, table_code, ids, subject_id=None):
        self.select = CellSelect.get_subject_select(item, table_code, STU_CODE, get_subject_code(subject_id))
        self.fixed_where = CellWhere.get_subject_fixed_where(subject_id)
        self.varied_where = [greater_where, less_equal_where]
        self.ids = ids

    def get_value(self):
        where = CellWhere(self.varied_where, self.fixed_where)
        cell = CellFactory.get_cell(self.select, where)
        return ValueFactory.get_row_value(cell, self.ids)[0]


class AllDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, ids, subject_id=None):
        super(AllDistributionValue, self).__init__(item, table_code, ids[1:], subject_id)
        self.o_varied_where = [greater_equal_where, less_equal_where]
        self.o_ids = ids[0:1]

    def get_value(self):
        where = CellWhere(self.o_varied_where, self.fixed_where)
        cell = CellFactory.get_cell(self.select, where)
        greater_value = super(AllDistributionValue, self).get_value()
        greater_equal_value = ValueFactory.get_row_value(cell, self.o_ids)[0]
        return list_util.combine_values_by_col([greater_equal_value], [greater_value])[0]


class CountDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, ids, count):
        super(CountDistributionValue, self).__init__(item, table_code, ids, None)
        count_where.set_value(count)
        self.fixed_where.append(count_where)


class NormalColValue(object):
    def __init__(self, item, table_code, district_code, subject_id=None, id_code=None):
        self.select = CellSelect.get_subject_select(item, table_code, district_code, get_subject_code(subject_id))
        if id_code is None:
            self.varied_where = CellWhere.get_district_varied_where(district_code)
            self.ids = get_district_varied_ids(district_code)
        else:
            self.varied_where = CellWhere.get_district_varied_where(id_code)
            self.ids = get_district_varied_ids(id_code)
        self.fixed_where = CellWhere.get_subject_fixed_where(subject_id)

    def get_value(self):
        where = CellWhere(self.varied_where, self.fixed_where)
        cell = CellFactory.get_cell(self.select, where)
        return ValueFactory.get_col_value(cell, self.ids)


def print_rows(rows):
    for row in rows:
        print(row)


if __name__ == '__main__':
    subject_id = 121
    subject_name = "语文"

    dimen_order_value = OrderValue(item_config.AVG_ITEM, DISTRICT_CODE, QA_CODE)
    print_rows(dimen_order_value.get_subject_value())
    print_rows(dimen_order_value.get_exam_value(subject_id))

    print()

    school_std_value = OneRowValue(item_config.AVG_RATIO_ITEM % 150, QA_ZK_CODE, SCHOOL_CODE, subject_id=subject_id)
    print(school_std_value.get_value())

    print()

    distribution_ids, distribution_names = get_distributions(subject_name)
    distribution_values = ScoreDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = AllDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = CountDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids, 5).get_value()
    print(distribution_values, sum(distribution_values))

    print()
    district_sum = OneRowValue('avg', QA_ZK_CODE, DISTRICT_CODE)
    school_sum = OneRowValue('avg', QA_ZK_CODE, SCHOOL_CODE)
    print(district_sum.get_value())
    print(school_sum.get_value())

    print()

    school_stu_sum = NormalColValue(item_config.SUM_ITEM, QA_ZK_CODE, STU_CODE, id_code=SCHOOL_CODE)
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)
    school_stu_sum = NormalColValue(item_config.SUM_ITEM, QA_ZK_CODE, STU_CODE, subject_id=subject_id,
                                    id_code=SCHOOL_CODE)
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)

    print()

    school_dimen_avg = NormalColValue(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, DISTRICT_CODE,
                                      subject_id=subject_id)
    school_dimen_avg_value = school_dimen_avg.get_value()
    print_rows(school_dimen_avg_value)
