import refactoring.edu.service.rows_service as rows_service
import refactoring.edu.domain.qa as qa
import refactoring.edu.dao.qam_dao as qam_dao

SPECIAL = 1
CURRENT = 2

NULL_ITEM = "''"
NUM_ITEM = "num_nz"
AVG_ITEM = 'ROUND(avg, 2)'
RANK_ITEM = 'rank'
AVG_NULL_ITEM = [AVG_ITEM, NULL_ITEM]
AVG_RANK_ITEM = [AVG_ITEM, RANK_ITEM]

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

DISTRICT_AVG_RANK_OF_SUM_SUBJECT = ['类别', '总分', '排名', '语文', '排名', '数学', '英语', '排名', '物理', '排名', '化学', '排名']


def district_avg_rank_of_sum_subject(exam_where, subject_ids, district_ids, school_ids, district_names, school_names,
                                     type_code):
    district_where = qa.Where("district")
    school_where = qa.Where("school")
    dimen_table = QA_DISTRICT_DIMEN_TABLE
    sum_table = QA_DISTRICT_SUM_TABLE
    district_subject_values = rows_service.table_of_dimen_sum_values(AVG_NULL_ITEM, dimen_table, exam_where,
                                                                     district_where,
                                                                     district_ids, subject_ids)
    district_sum_values = rows_service.table_of_dimen_sum_values(AVG_NULL_ITEM, sum_table, exam_where, district_where,
                                                                 district_ids)


class ExamTableData(object):
    def __init__(self, exam):
        self.exam = exam

        self.school_id = qam_dao.get_all_school_ids_order(exam, QA_SCHOOL_SUM_TABLE)
        self.school_names = qam_dao.get_all_school_names_order(exam, QA_SCHOOL_SUM_TABLE)


