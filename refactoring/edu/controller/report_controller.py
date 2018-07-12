import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
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

class_ids, class_names = report_config.get_class_ids()
grade_lev = report_config.grade_lev
exam_id = report_config.exam_id
exam_where = qa.Where("examId", exam_id)

district_where = qa.Where("districtId", 9)
school_where = qa.Where("schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
subject_where = qa.Where("subjectId", 121)
class_where = qa.Where('classId', "0A036FDF66274D31B8DEC6F7E07A820F")

greater_where = qa.Where("sum", symbol=">")
less_equal_where = qa.Where("sum", symbol="<=")
greater_equal_where = qa.Where("sum", symbol=">=")
count_where = qa.Where("count")

font_exam_where = qa.Where("font.examId")
behind_exam_where = qa.Where("behind.examId")
font_school_where = qa.Where("font.schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
behind_school_where = qa.Where("behind.schoolId", "002F2A5004B9421EBEC2AAD8A6CEB044")
font_subject_where = qa.Where("font.subjectId", 121)
behind_subject_where = qa.Where("behind.subjectId", 121)

district_len = len(district_ids)
school_len = len(school_ids)
class_len = len(class_ids)

enroll_year = report_config.enroll_year
all_exam_ids = qam_dao.get_exam_ids(enroll_year, grade_lev)
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

GREATER_EQUAL = 1
GREATER = 2


def get_exam_diff_ids(exam_ids):
    length = len(exam_ids)

    result = []
    for index in range(length - 1):
        result.append([exam_ids[index], exam_ids[index + 1]])
    if length > 2:
        result.append([exam_ids[0], exam_ids[- 1]])
    return result


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


def get_subject_exam_ids(subject_id):
    return all_exam_ids[0:4]


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


class WhereFactory(object):
    @staticmethod
    def get_district_varied_where(district_code):
        if district_code == DISTRICT_CODE:
            return district_where
        elif district_code == SCHOOL_CODE:
            return school_where
        elif district_code == CLASS_CODE:
            return [school_where, class_where]

    @staticmethod
    def combine_subject_with_other(subject, orther):
        result = [orther]
        if subject is not None:
            result.append(subject)
        return result

    @staticmethod
    def get_exam_subject_fixed_where(subject_id=None):
        subject = WhereFactory.get_subject_fixed_where(subject_id)
        return WhereFactory.combine_subject_with_other(subject, exam_where)

    @staticmethod
    def get_subject_fixed_where(subject_id=None):
        if subject_id is None:
            return None
        else:
            subject_where.set_value(subject_id)
            return subject_where

    @staticmethod
    def get_district_fixed_where(district_code, id):
        result = WhereFactory.get_district_varied_where(district_code)
        result.set_value(id)
        return result

    @staticmethod
    def get_district_subject_fixed_where(district_code, id, subject_id):
        district = WhereFactory.get_district_fixed_where(district_code, id)
        subject = WhereFactory.get_subject_fixed_where(subject_id)
        return WhereFactory.combine_subject_with_other(subject, district)

    @staticmethod
    def get_school_diff_subject_fixed_where(school_id, subject_id):
        font_school_where.set_value(school_id)
        font_subject_where.set_value(subject_id)
        behind_school_where.set_value(school_id)
        behind_subject_where.set_value(subject_id)
        return [font_school_where, font_subject_where, behind_school_where, behind_subject_where]

    @staticmethod
    def get_count_fixed_where(count):
        count_where.set_value(count)
        return count_where


class CellOrder(object):
    def __init__(self, item, ids):
        self.item = item
        self.ids = ids


class ValueCell(object):
    def __init__(self):
        self.item = None
        self.table = None
        self.varied_where = None
        self.fixed_where = None
        self.ids = None

    def get_where_list(self):
        where_list = [self.varied_where]
        if isinstance(self.fixed_where, list):
            where_list += self.fixed_where
        else:
            where_list.append(self.fixed_where)
        return where_list

    def get_cell(self):
        return qa.Cell(self.item, self.table, self.get_where_list())


class OrderValueCell(ValueCell):
    def __init__(self):
        super(OrderValueCell, self).__init__()
        self.order = None

    def get_cell(self):
        return qa.CellWithOrders(self.item, self.table, self.get_where_list(),
                                 self.order.item, self.order.ids)


class RowValue(ValueCell):
    def __init__(self):
        super(RowValue, self).__init__()

    def get_value(self):
        return qa.RowSeriesCell(self.get_cell(), self.ids).get_values()


class ColValue(ValueCell):
    def __init__(self):
        super(ColValue, self).__init__()

    def get_value(self):
        return qa.ColSeriesCell(self.get_cell(), self.ids).get_values()


class OrderColValue(OrderValueCell):
    def __init__(self):
        super(OrderColValue, self).__init__()

    def get_value(self):
        return qa.ColSeriesCell(self.get_cell(), self.ids).get_values()


class DistrictExamSubjectOrderValue(OrderColValue):
    def __init__(self, item, table_code, district_code):
        self.item = item
        self.table = table_config.get_subject_score_table_name(table_code, district_code)
        self.varied_where = WhereFactory.get_district_varied_where(district_code)
        self.ids = get_district_varied_ids(district_code)


class ExamSubjectOrderValue(DistrictExamSubjectOrderValue):
    def __init__(self, item, table_code, district_code):
        super(ExamSubjectOrderValue, self).__init__(item, table_code, district_code)
        self.fixed_where = exam_where
        self.order = CellOrder("subjectId", subject_ids)


class SubjectExamOrderValue(DistrictExamSubjectOrderValue):
    def __init__(self, item, table_code, district_code, subject_id):
        super(SubjectExamOrderValue, self).__init__(item, table_code, district_code)
        self.fixed_where = WhereFactory.get_subject_fixed_where(subject_id)
        self.order = CellOrder("examId", get_subject_exam_ids(subject_id))


class OneRowValue(RowValue):
    def __init__(self, item, table_code, district_code, subject_id=None):
        self.item = item
        self.table = table_config.get_score_table_name(table_code, district_code, get_subject_code(subject_id))
        self.fixed_where = WhereFactory.get_exam_subject_fixed_where(subject_id)
        self.varied_where = WhereFactory.get_district_varied_where(district_code)
        self.ids = get_district_varied_ids(district_code)


class ScoreDistributionValue(OneRowValue):
    def __init__(self, item, table_code, ids, subject_id=None):
        super(ScoreDistributionValue, self).__init__(item, table_code, STU_CODE, subject_id)
        self.varied_where = [greater_where, less_equal_where]
        self.ids = ids


class AllDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, ids, subject_id=None):
        super(AllDistributionValue, self).__init__(item, table_code, ids[1:], subject_id)

        greater_equal_value = ScoreDistributionValue(item, table_code, ids[0:1], subject_id)
        greater_equal_value.varied_where = [greater_equal_where, less_equal_where]
        self.values = greater_equal_value.get_value()

    def get_value(self):
        return list_util.to_a_list([self.values, super(AllDistributionValue, self).get_value()])


class CountDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, ids, count):
        super(CountDistributionValue, self).__init__(item, table_code, ids, None)
        self.fixed_where.append(WhereFactory.get_count_fixed_where(count))


class ExamSubjectDistirct(ColValue):
    def __init__(self, item, district_code, subject_id=None):
        self.item = item
        self.varied_where = WhereFactory.get_district_varied_where(district_code)
        self.fixed_where = WhereFactory.get_exam_subject_fixed_where(subject_id)
        self.ids = get_district_varied_ids(district_code)


class SchoolStu(ExamSubjectDistirct):
    def __init__(self, item, table_code, subject_id=None):
        super(SchoolStu, self).__init__(item, SCHOOL_CODE, subject_id)
        self.table = table_config.get_stu_score_table(table_code, get_subject_code(subject_id))


class ExamDimenValue(ExamSubjectDistirct):
    def __init__(self, item, table_code, district_code, subject_id):
        super(ExamDimenValue, self).__init__(item, district_code, subject_id)
        self.table = table_config.get_subject_score_table_name(table_code, district_code)


class ExamSchoolLineValue(ExamSubjectDistirct):
    def __init__(self, item, table_code):
        super(ExamSchoolLineValue, self).__init__(item, SCHOOL_CODE, None)
        self.table = table_config.get_school_sum_line(table_code)


class SubjectDimenValue(ColValue):
    def __init__(self, item, table_code, district_code, id, subject_id):
        self.item = item
        self.table = table_config.get_subject_score_table_name(table_code, district_code)
        self.fixed_where = WhereFactory.get_district_subject_fixed_where(district_code, id, subject_id)
        self.varied_where = exam_where
        self.ids = get_subject_exam_ids(subject_id)


class DimenDiffValue(ColValue):
    def __init__(self, item, table_code, school_id, subject_id):
        self.item = item
        self.table = table_config.get_school_rank_diff_table(table_code)
        self.fixed_where = WhereFactory.get_school_diff_subject_fixed_where(school_id, subject_id)
        self.varied_where = [font_exam_where, behind_exam_where]
        self.ids = get_exam_diff_ids(get_subject_exam_ids(subject_id))


def print_rows(rows):
    for row in rows:
        print(row)


if __name__ == '__main__':
    d1 = datetime.datetime.now()
    subject_id = 121
    subject_name = "语文"

    dimen_order_value = ExamSubjectOrderValue(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE)
    print_rows(dimen_order_value.get_value())
    dimen_order_value = SubjectExamOrderValue(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE, subject_id)
    print_rows(dimen_order_value.get_value())

    print()

    school_std_value = OneRowValue(item_config.AVG_RATIO_ITEM % 150, QA_ZK_CODE, SCHOOL_CODE, subject_id=subject_id)
    print(school_std_value.get_value())

    print()

    distribution_ids, distribution_names = get_distributions(subject_name)
    distribution_values = ScoreDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = AllDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = CountDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, distribution_ids,
                                                 5).get_value()
    print(distribution_values, sum(distribution_values))

    print()
    district_sum = OneRowValue('avg', QA_ZK_CODE, DISTRICT_CODE)
    school_sum = OneRowValue('avg', QA_ZK_CODE, SCHOOL_CODE)
    class_sum = OneRowValue('avg', QA_ZK_CODE, CLASS_CODE)
    print(district_sum.get_value())
    print(school_sum.get_value())
    print(class_sum.get_value())

    print()

    school_stu_sum = SchoolStu(item_config.SUM_ITEM, QA_ZK_CODE)
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)
    school_stu_sum = SchoolStu(item_config.SUM_ITEM, QA_ZK_CODE, subject_id=subject_id)
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)

    print()

    school_dimen_avg = ExamDimenValue(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, DISTRICT_CODE,
                                      subject_id)
    print(school_dimen_avg.get_value())
    subject_dimen = SubjectDimenValue(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, SCHOOL_CODE,
                                      school_ids[0], subject_id)
    print(subject_dimen.get_value())

    print()

    school_line = ExamSchoolLineValue(item_config.LINE_25_60_85_ITEMS, QA_ZK_CODE)
    print(school_line.get_value())

    print()

    dimen_rank_diff = DimenDiffValue(item_config.DIMEN_RANK_DIFF_ITEMS[0:8], QA_ZK_CODE, school_ids[0], subject_id)
    print_rows(dimen_rank_diff.get_value())
    d2 = datetime.datetime.now()
    print(d2 - d1)
