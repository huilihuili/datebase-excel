import refactoring.edu.dao.qam_dao as qam_dao
import refactoring.edu.config.table_config as table_config

#########################################################

SPECIAL = 1  # 以special名单为准(初三一模)
CURRENT = 2  # 以本次考试名单为准(初三二模)

#########################################################

LINE_ITEMS_2 = ["line25", "line60", "line85"]

SUBJECT_IDS_2 = [121, 122, 103, 118, 128]
SUBJECT_NAMES_2 = ['语文', '数学', '英语', '物理', '化学']

DISTRICT_IDS_2 = ['9', '1', '2']
DISTRICT_NAMES_2 = ['全区', '公办', '民办']

EXAM_NICKS_2 = ["初中预备", "初一期末", "初二期末", "初三一模", "初三二模"]

ALL = 1
SCORE = 2
COUNT = 3

DISTRIBUTION_SCORE_150 = [SCORE, [[0, 150, 5], ]]
DISTRIBUTION_SCORE_100 = [SCORE, [[0, 100, 5], ]]
DISTRIBUTION_SCORE_90 = [SCORE, [[0, 90, 5], ]]
DISTRIBUTION_SCORE_60 = [SCORE, [[0, 60, 5], ]]
DISTRIBUTION_COUNT_650_5 = [COUNT, [[0, 120, 120], [120, 650, 5], ], 5]
DISTRIBUTION_COUNT_600_5 = [COUNT, [[0, 120, 120], [120, 600, 5], ], 5]

MAIN_SUBJECTA_TOTAL = {
    "语文": 150,
    "数学": 150,
    "英语": 150,
}

VARIED_SUBJECT_TOTAL = {
    "初三一模": {
        "物理": 100,
        "化学": 100,
        "总分": 650,
    },
    "初三二模": {
        "物理": 90,
        "化学": 60,
        "总分": 600,
    },
}

MAIN_SUBJECTA_DISTRIBUTION = {
    "语文": DISTRIBUTION_SCORE_150,
    "数学": DISTRIBUTION_SCORE_150,
    "英语": DISTRIBUTION_SCORE_150,
}

VARIED_SUBJECT_DISTRIBUTIONS = {
    "初三一模": {
        "物理": DISTRIBUTION_SCORE_100,
        "化学": DISTRIBUTION_SCORE_100,
        "总分": DISTRIBUTION_COUNT_650_5,
    },
    "初三二模": {
        "物理": DISTRIBUTION_SCORE_90,
        "化学": DISTRIBUTION_SCORE_60,
        "总分": DISTRIBUTION_COUNT_600_5,
    },
}

CHART_EXTRA_TITLE = {
    2: {
        table_config.QAT_CODE: "实考",
        table_config.QA_ZK_CODE: "(参与中考)"
    },
}

TABLE_EXTRA_TITLE = {
    2: {
        table_config.QA_CODE: "(实考)",
        table_config.QA_ZK_CODE: "(中考)"
    },
}


#########################################################


def get_subject_info():
    if grade_lev == 2:
        return SUBJECT_IDS_2, SUBJECT_NAMES_2


def get_district_info():
    if grade_lev == 2:
        return DISTRICT_IDS_2, DISTRICT_NAMES_2


def get_school_info():
    return qam_dao.get_all_school_ids_order(grade_lev, exam_id, "qa_school_sum"), \
           qam_dao.get_all_school_names_order(grade_lev, exam_id, "qa_school_sum")


def get_school_type():
    return qam_dao.get_all_school_types_order(grade_lev, exam_id, "qa_school_sum")


def get_class_ids():
    if base_student == SPECIAL:
        table_name = "qa_zk_class_sum"
    elif base_student == CURRENT:
        table_name = "qa_class_sum"
    return qam_dao.get_all_school_class_ids(grade_lev, exam_id, table_name), qam_dao.get_all_school_class_names(
        grade_lev, exam_id,
        table_name)


def get_distribution(subject_name):
    if subject_name in MAIN_SUBJECTA_DISTRIBUTION.keys():
        return MAIN_SUBJECTA_DISTRIBUTION[subject_name]
    else:
        return VARIED_SUBJECT_DISTRIBUTIONS[exam_nick][subject_name]


def get_total(subject_name):
    if subject_name in MAIN_SUBJECTA_TOTAL.keys():
        return MAIN_SUBJECTA_TOTAL[subject_name]
    else:
        return VARIED_SUBJECT_TOTAL[exam_nick][subject_name]


def get_table_extra_title(type_code):
    return TABLE_EXTRA_TITLE[grade_lev][type_code]


def get_chart_extra_title(type_code):
    return CHART_EXTRA_TITLE[grade_lev][type_code]


#########################################################

grade_lev = 2
base_student = SPECIAL

exam_id = '8c4646637f44489c9ba9333e580fe9d0'
enroll_year = 2014
exam_nick = '初三一模'

#########################################################

if __name__ == '__main__':
    print(get_distribution("语文"))
    print(get_distribution("物理"))
