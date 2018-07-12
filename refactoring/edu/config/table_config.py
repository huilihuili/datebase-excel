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

QA_CODE = 1
QA_ZK_CODE = 2
QAT_CODE = 3

DISTRICT_CODE = 1
SCHOOL_CODE = 2
CLASS_CODE = 3
STU_CODE = 4

SUBJECT_CODE = 1
SUM_CODE = 2

SCORE_CODE = 1
LINE_CODE = 2


def get_table_name(table_code, district_code, subject_code, score_code):
    if score_code == SCORE_CODE:
        return get_score_table_name(table_code, district_code, subject_code)
    elif score_code == LINE_CODE:
        return get_line_table_name(table_code, district_code, subject_code)


#########################################################

def get_score_table_name(table_code, district_code, subject_code):
    if subject_code == SUBJECT_CODE:
        return get_subject_score_table_name(table_code, district_code)
    elif subject_code == SUM_CODE:
        return get_sum_score_table_name(table_code, district_code)


def get_line_table_name(table_code, district_code, subject_code):
    if subject_code == SUM_CODE:
        return get_sum_line_table_name(table_code, district_code)


#########################################################


def get_subject_score_table_name(table_code, district_code):
    if district_code == DISTRICT_CODE:
        return get_district_dimen_table(table_code)
    elif district_code == SCHOOL_CODE:
        return get_school_dimen_table(table_code)
    elif district_code == CLASS_CODE:
        return get_class_dimen_table()
    elif district_code == STU_CODE:
        return get_stu_dimen_table(table_code)


def get_sum_score_table_name(table_code, district_code):
    if district_code == DISTRICT_CODE:
        return get_district_sum_table(table_code)
    elif district_code == SCHOOL_CODE:
        return get_school_sum_table(table_code)
    elif district_code == CLASS_CODE:
        return get_class_sum_table(table_code)
    elif district_code == STU_CODE:
        return get_stu_sum_table(table_code)


def get_sum_line_table_name(table_code, district_code):
    if district_code == SCHOOL_CODE:
        return get_school_sum_line(table_code)


#########################################################

def get_stu_score_table(table_code, subject_code):
    if subject_code == SUM_CODE:
        return get_stu_sum_table(table_code)
    elif subject_code == SUBJECT_CODE:
        return get_stu_dimen_table(table_code)


#########################################################

def get_district_dimen_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_DISTRICT_DIMEN_TABLE
    elif table_code == QA_CODE:
        return QA_DISTRICT_DIMEN_TABLE
    elif table_code == QAT_CODE:
        return QAT_DISTRICT_DIMEN_TABLE


def get_district_sum_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_DISTRICT_SUM_TABLE
    elif table_code == QA_CODE:
        return QA_DISTRICT_SUM_TABLE


def get_school_dimen_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_SCHOOL_DIMEN_TABLE
    elif table_code == QA_CODE:
        return QA_SCHOOL_DIMEN_TABLE
    elif table_code == QAT_CODE:
        return QAT_SCHOOL_DIMEN_TABLE


def get_school_sum_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_SCHOOL_SUM_TABLE
    elif table_code == QA_CODE:
        return QA_SCHOOL_SUM_TABLE


def get_school_sum_line(table_code):
    if table_code == QA_CODE:
        return QA_SCHOOL_LINE_TABLE
    elif table_code == QA_ZK_CODE:
        return QA_SCHOOL_LINE_TABLE


def get_class_dimen_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_CLASS_DIMEN_TABLE
    elif table_code == QA_CODE:
        return QA_CLASS_DIMEN_TABLE


def get_class_sum_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_CLASS_SUM_TABLE
    elif table_code == QA_CODE:
        return QA_CLASS_SUM_TABLE


def get_stu_dimen_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_STU_DIMEN_TABLE
    elif table_code == QA_CODE:
        return QA_STU_DIMEN_TABLE


def get_stu_sum_table(table_code):
    if table_code == QA_ZK_CODE:
        return QA_ZK_STU_SUM_TABLE
    elif table_code == QA_CODE:
        return QA_STU_SUM_TABLE


def get_school_rank_diff_table(table_code):
    if table_code == QA_ZK_CODE:
        table = QA_ZK_SCHOOL_DIMEN_TABLE
    elif table_code == QAT_CODE:
        table = QAT_SCHOOL_DIMEN_TABLE
    return ["%s AS font" % table, "%s AS behind" % table]
