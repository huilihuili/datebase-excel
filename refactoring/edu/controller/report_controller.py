import refactoring.edu.config.item_config as item_config
import refactoring.edu.config.table_config as table_config
import refactoring.edu.util.list_util as list_util
import refactoring.edu.domain.qa as qa
import datetime

import refactoring.edu.entrance.handler as handler

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


def get_subject_code(subject_id):
    if subject_id is None:
        return SUM_CODE
    else:
        return SUBJECT_CODE


class ValueCell(object):
    def __init__(self, exam, where):
        self.item = None
        self.table = None
        self.where = where
        self.ids = None
        self.exam = exam
        # self.where = handler.Where()
        # self.exam = handler.Exam()

    def get_where_list(self):
        where_list = [self.where.varied]
        if isinstance(self.where.fixed, list):
            where_list += self.where.fixed
        else:
            where_list.append(self.where.fixed)
        return where_list

    def get_cell(self):
        where_list = qa.MainWhere(self.where.fixed, self.where.varied)
        return qa.Cell(self.item, self.table, where_list)


class OrderValueCell(ValueCell):
    def __init__(self, exam, where):
        super(OrderValueCell, self).__init__(exam, where)
        self.order = None

    def get_cell(self):
        where_list = qa.MainWhere(self.where.fixed, self.where.varied)
        return qa.CellWithOrders(self.item, self.table, where_list,
                                 self.order)


class RowValue(ValueCell):
    def __init__(self, exam, where):
        super(RowValue, self).__init__(exam, where)

    def get_value(self):
        return qa.RowSeriesCell(self.get_cell(), self.ids).get_values()


class ColValue(ValueCell):
    def __init__(self, exam, where):
        super(ColValue, self).__init__(exam, where)

    def get_value(self):
        return qa.ColSeriesCell(self.get_cell(), self.ids).get_values()


class OrderColValue(OrderValueCell):
    def __init__(self, exam, where):
        super(OrderColValue, self).__init__(exam, where)

    def get_value(self):
        return qa.ColSeriesCell(self.get_cell(), self.ids).get_values()


class DistrictExamSubjectOrderValue(OrderColValue):
    def __init__(self, item, table_code, district_code, exam, where):
        super(DistrictExamSubjectOrderValue, self).__init__(exam, where)
        self.item = item
        self.table = table_config.get_subject_score_table_name(table_code, district_code)
        self.where.set_district_varied(district_code)
        self.ids = self.exam.get_district_varied_ids(district_code)


class ExamSubjectOrderValue(DistrictExamSubjectOrderValue):
    def __init__(self, item, table_code, district_code, exam, where):
        super(ExamSubjectOrderValue, self).__init__(item, table_code, district_code, exam, where)
        self.where.set_exam_fixed()
        self.order = qa.CellOrder("subjectId", self.exam.gradation.subject_ids)


class SubjectExamOrderValue(DistrictExamSubjectOrderValue):
    def __init__(self, item, table_code, district_code, subject_id, exam, where):
        super(SubjectExamOrderValue, self).__init__(item, table_code, district_code, exam, where)
        self.where.set_subject_fixed(subject_id)
        self.order = qa.CellOrder("examId", self.exam.get_subject_exam_ids(subject_id))


class OneRowValue(RowValue):
    def __init__(self, item, table_code, district_code, exam, where, subject_id=None):
        super(OneRowValue, self).__init__(exam, where)
        self.item = item
        self.table = table_config.get_score_table_name(table_code, district_code, get_subject_code(subject_id))
        self.where.set_exam_subject_fixed(subject_id)
        self.where.set_district_varied(district_code)
        self.ids = self.exam.get_district_varied_ids(district_code)


class ScoreDistributionValue(OneRowValue):
    def __init__(self, item, table_code, exam, where, subject_id=None):
        super(ScoreDistributionValue, self).__init__(item, table_code, STU_CODE, exam, where, subject_id)
        self.where.set_greater_less_equal_varied()
        self.ids = self.exam.get_subject_distribution_ids(subject_id)


class AllDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, exam, where, subject_id=None):
        super(AllDistributionValue, self).__init__(item, table_code, exam, where, subject_id)
        temp = self.ids.copy()
        self.ids = temp[1:]

        greater_equal_value = ScoreDistributionValue(item, table_code, exam, where, subject_id)
        greater_equal_value.ids = temp[0:1]
        greater_equal_value.where.set_greater_equal_less_equal_varied()
        self.values = greater_equal_value.get_value()

    def get_value(self):
        return list_util.to_a_list([self.values, super(AllDistributionValue, self).get_value()])


class CountDistributionValue(ScoreDistributionValue):
    def __init__(self, item, table_code, exam, where):
        super(CountDistributionValue, self).__init__(item, table_code, exam, where, None)
        self.where.set_exam_subject_count_fixed_where(self.exam.count)


class ExamSubjectDistirct(ColValue):
    def __init__(self, item, district_code, exam, where, subject_id=None):
        super(ExamSubjectDistirct, self).__init__(exam, where)
        self.item = item
        self.where.set_district_varied(district_code)
        self.where.set_exam_subject_fixed(subject_id)
        self.ids = self.exam.get_district_varied_ids(district_code)


class SchoolStu(ExamSubjectDistirct):
    def __init__(self, item, table_code, exam, where, subject_id=None):
        super(SchoolStu, self).__init__(item, SCHOOL_CODE, exam, where, subject_id)
        self.table = table_config.get_stu_score_table(table_code, get_subject_code(subject_id))


class ExamDimenValue(ExamSubjectDistirct):
    def __init__(self, item, table_code, district_code, exam, where, subject_id):
        super(ExamDimenValue, self).__init__(item, district_code, exam, where, subject_id)
        self.table = table_config.get_subject_score_table_name(table_code, district_code)


class ExamSchoolLineValue(ExamSubjectDistirct):
    def __init__(self, item, table_code, exam, where):
        super(ExamSchoolLineValue, self).__init__(item, SCHOOL_CODE, exam, where, None)
        self.table = table_config.get_school_sum_line(table_code)


class SubjectDimenValue(ColValue):
    def __init__(self, item, table_code, district_code, id, exam, where, subject_id):
        super(SubjectDimenValue, self).__init__(exam, where)
        self.item = item
        self.table = table_config.get_subject_score_table_name(table_code, district_code)
        self.where.set_district_subject_fixed(district_code, id, subject_id)
        self.where.set_exam_fixed()
        self.ids = self.exam.get_subject_exam_ids(subject_id)


class DimenDiffValue(ColValue):
    def __init__(self, item, table_code, school_id, exam, where, subject_id):
        super(DimenDiffValue, self).__init__(exam, where)
        self.item = item
        self.table = table_config.get_school_rank_diff_table(table_code)
        self.where.set_school_diff_subject_fixed(school_id, subject_id)
        self.where.set_exam_diff_varied()
        self.ids = self.exam.get_subject_exam_diff_ids(subject_id)


def print_rows(rows):
    for row in rows:
        print(row)


if __name__ == '__main__':
    d1 = datetime.datetime.now()

    subject_id = 121
    subject_name = "语文"
    school_id = "002F2A5004B9421EBEC2AAD8A6CEB044"

    enroll_year = 2014
    grade_lev = 2
    gradation = handler.Gradation(enroll_year, grade_lev)

    exam_id = '8c4646637f44489c9ba9333e580fe9d0'
    base_student = handler.Exam.SPECIAL
    exam = handler.Exam(gradation, exam_id, base_student)

    where = handler.Where(exam.exam_id)

    dimen_order_value = ExamSubjectOrderValue(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE, exam, where)
    print_rows(dimen_order_value.get_value())
    dimen_order_value = SubjectExamOrderValue(item_config.AVG_ITEM, QA_CODE, DISTRICT_CODE, subject_id, exam, where)
    print_rows(dimen_order_value.get_value())

    print()

    school_std_value = OneRowValue(item_config.AVG_RATIO_ITEM % 150, QA_ZK_CODE, SCHOOL_CODE, exam, where,
                                   subject_id=subject_id)
    print(school_std_value.get_value())

    print()

    distribution_values = ScoreDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, exam, where).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = AllDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE, exam, where).get_value()
    print(distribution_values, sum(distribution_values))
    distribution_values = CountDistributionValue(item_config.COUNT_ITEM, QA_ZK_CODE,
                                                 exam, where).get_value()
    print(distribution_values, sum(distribution_values))

    print()
    district_sum = OneRowValue('avg', QA_ZK_CODE, DISTRICT_CODE, exam, where)
    print(district_sum.get_value())
    school_sum = OneRowValue('avg', QA_ZK_CODE, SCHOOL_CODE, exam, where)
    print(school_sum.get_value())
    class_sum = OneRowValue('avg', QA_ZK_CODE, CLASS_CODE, exam, where)
    print(class_sum.get_value())

    print()

    school_stu_sum = SchoolStu(item_config.SUM_ITEM, QA_ZK_CODE, exam, where, )
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)
    school_stu_sum = SchoolStu(item_config.SUM_ITEM, QA_ZK_CODE, exam, where, subject_id=subject_id)
    school_stu_sum_values = school_stu_sum.get_value()
    print(len(school_stu_sum_values), school_stu_sum_values)

    print()

    school_dimen_avg = ExamDimenValue(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, DISTRICT_CODE,
                                      exam, where, subject_id)
    print(school_dimen_avg.get_value())
    subject_dimen = SubjectDimenValue(item_config.DIMEN_AVG_ITEMS[0:8], QA_ZK_CODE, SCHOOL_CODE,
                                      school_id, exam, where, subject_id)
    print(subject_dimen.get_value())

    print()

    school_line = ExamSchoolLineValue(item_config.LINE_25_60_85_ITEMS, QA_ZK_CODE, exam, where, )
    print(school_line.get_value())

    print()

    dimen_rank_diff = DimenDiffValue(item_config.DIMEN_RANK_DIFF_ITEMS[0:8], QA_ZK_CODE, school_id, exam, where,
                                     subject_id)
    print_rows(dimen_rank_diff.get_value())
    d2 = datetime.datetime.now()
    print(d2 - d1)
