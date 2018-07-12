import refactoring.edu.domain.qa as qa
import refactoring.edu.domain.qam as qam
import refactoring.edu.dao.qam_dao as qam_dao
import refactoring.edu.util.list_util as list_util
import refactoring.edu.config.report_config as config

subject_ids = [121, 122, 103, 118, 128]
subject_names = ['语文', '数学', '英语', '物理', '化学']


class BaseStudent(object):
    NORMAL = 1  # qa
    SPECIAL = 2  # qa_zk
    CURRENT = 3  # qat

    @staticmethod
    def get_table_str(table_code):
        if table_code == BaseStudent.NORMAL:
            return "qa"
        if table_code == BaseStudent.SPECIAL:
            return "qa_zk"
        elif table_code == BaseStudent.CURRENT:
            return "qat"


class Subject(object):
    SUBJECT = 1
    SUM = 2

    @staticmethod
    def get_dimen(subject_code):
        if subject_code == Subject.SUBJECT:
            return "dimen"
        elif subject_code == Subject.SUM:
            return "sum"

    @staticmethod
    def get_line(subject_code):
        if subject_code == TableName.SUBJECT:
            return "subject"
        else:
            return ""


class FirstRow(object):
    AVG_RANK_OF_SUM_SUBJECT = ['类别', '总分', '排名', '语文', '排名', '数学', '英语', '排名', '物理', '排名', '化学', '排名']


class District(object):
    DISTRICT = 1
    SCHOOL = 2
    CLASS = 3
    STU = 4

    @staticmethod
    def get_district_str(district_code):
        if district_code == District.DISTRICT:
            return "district"
        elif district_code == District.SCHOOL:
            return "school"
        elif district_code == District.CLASS:
            return "class"
        elif district_code == District.STU:
            return "stu"


class Item(object):
    @staticmethod
    def get_sum_str(sum_count):
        if sum_count == 5:
            return "five"
        elif sum_count == 3:
            return "three"

    @staticmethod
    def get_sum_avg(sum_count):
        return "ROUND(avg_%s, 2)" % Item.get_sum_str(sum_count)

    @staticmethod
    def get_sum_rank(sum_count):
        return "rank_%s" % (Item.get_sum_str(sum_count))

    @staticmethod
    def get_sum_avg_null(sum_count):
        return [Item.get_sum_avg(sum_count), Item.NULL]

    SUBJECT_AVG = "ROUND(avg, 2)"
    NULL = "''"
    SUBJECT_AVG_NULL = [SUBJECT_AVG, NULL]
    SUBJECT = "subjectId"


class TableName(object):
    @staticmethod
    def dimen(table_code, district_code, subject_code):
        table_str = BaseStudent.get_table_str(table_code)
        district_str = District.get_district_str(district_code)
        score_str = Subject.get_dimen(subject_code)
        return "%s_%s_%s" % (table_str, district_str, score_str)

    @staticmethod
    def line_num(table_code, district_code, subject_code):
        table_str = BaseStudent.get_table_str(table_code)
        district_str = District.get_district_str(district_code)
        score_str = Subject.get_line(subject_code)

        line_str = ""
        if district_code == TableName.DISTRICT:
            line_str = "line_num"
        elif district_code == TableName.SCHOOL:
            line_str = "line"
        return "%s_%s_%s_%s" % (table_str, score_str, district_str, line_str)


class WhereFactory(object):

    @staticmethod
    def exam(value=""):
        return qa.Where("examId", value=value)

    @staticmethod
    def district(value=""):
        return qa.Where("districtId", value=value)

    @staticmethod
    def school(value=""):
        return qa.Where("schoolId", value=value)

    @staticmethod
    def subject(value=""):
        return qa.Where("subjectId", value=value)


class ReportController(object):
    district_names = []
    district_ids = []

    school_names = []
    school_ids = []

    def __init__(self, exam, base_code, sum_count):
        self.exam = exam
        self.sum_count = sum_count
        self.base_code = base_code

        ReportController.district_names = qam_dao.get_all_district_names()
        ReportController.district_ids = qam_dao.get_all_district_ids()
        self.set_school_info()

    def avg_rank_of_subject_sum_of_districts_schools(self):
        district_dimen_table = TableName.dimen(BaseStudent.NORMAL, District.DISTRICT, Subject.SUBJECT)
        exam_where = WhereFactory.exam(self.exam.exam_id)
        district_subject_cell = qa.CellWithOrders(Item.SUBJECT_AVG_NULL, district_dimen_table,
                                                  [WhereFactory.district(), exam_where],
                                                  Item.SUBJECT, subject_ids)

        district_subject_row = qa.ColSeriesCell(district_subject_cell, ReportController.district_ids)

        district_sum_table = TableName.dimen(BaseStudent.NORMAL, District.DISTRICT, Subject.SUM)
        district_sum_cell = qa.Cell(Item.get_sum_avg_null(self.sum_count), district_sum_table,
                                    [WhereFactory.district(), exam_where])

        district_sum_row = qa.ColSeriesCell(district_sum_cell, ReportController.district_ids)

        datarows = qa.DataRows.combine_col_rows(district_sum_row, district_subject_row)
        district_names = list_util.add_something_to_list("（实考）", ReportController.district_names)
        for table_row in list_util.combine_values_by_row(FirstRow.AVG_RANK_OF_SUM_SUBJECT,
                                                         list_util.combine_values_by_col(district_names, datarows)):
            print(table_row)

    def set_school_info(self):
        base_code = 0
        if self.base_code == BaseStudent.SPECIAL:
            base_code = BaseStudent.SPECIAL
        elif self.base_code == BaseStudent.CURRENT:
            base_code = BaseStudent.NORMAL

        table_name = TableName.dimen(base_code, District.SCHOOL, Subject.SUM)
        exam_id = self.exam.exam_id
        grade_lev = qam.ExamInfo.grade_lev
        sum_rank = Item.get_sum_rank(self.sum_count)

        ReportController.school_names = qam_dao.get_all_school_names_order(table_name, exam_id, grade_lev, sum_rank)
        ReportController.school_ids = qam_dao.get_all_school_ids_order(table_name, exam_id, grade_lev, sum_rank)


if __name__ == '__main__':
    print("gradeLev =", config.grade_lev)
    if config.trigger_mode == config.ID_TRIGGER:
        exam = qam_dao.get_exam_by_id("8c4646637f44489c9ba9333e580fe9d0")
    elif config.trigger_mode == config.NICK_TRIGGER:
        exam = qam_dao.get_exam_by_nick(config.enroll_year, config.grade_lev, config.exam_nick)
    print("base student =", "cuttent" if config.base_student == config.CURRENT else "special")
    print(exam)
