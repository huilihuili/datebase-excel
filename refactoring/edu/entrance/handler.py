import refactoring.edu.dao.qam_dao as qam_dao
import refactoring.edu.dao.base_dao as base_dao
import refactoring.edu.util.list_util as list_util
import refactoring.edu.config.table_config as table_config
import refactoring.edu.domain.qa as qa

import datetime


class Gradation(object):
    DISTRICT_IDS_2 = ['9', '1', '2']
    DISTRICT_NAMES_2 = ['全区', '公办', '民办']

    SUBJECT_IDS_2 = [121, 122, 103, 118, 128]
    SUBJECT_NAMES_2 = ['语文', '数学', '英语', '物理', '化学']

    DISTRICT_CODE = 1
    SCHOOL_CODE = 2
    CLASS_CODE = 3
    STU_CODE = 4

    def __init__(self, enroll_year, grade_lev):
        self.enroll_year = enroll_year
        self.grade_lev = grade_lev

        self.district_ids = self.get_district_ids()
        self.district_names = self.get_district_names()
        self.subject_ids = self.get_subject_ids()
        self.subject_names = self.get_subject_names()

    def get_district_ids(self):
        if self.grade_lev == 2:
            return Gradation.DISTRICT_IDS_2

    def get_district_names(self):
        if self.grade_lev == 2:
            return Gradation.DISTRICT_NAMES_2

    def get_subject_ids(self):
        if self.grade_lev == 2:
            return Gradation.SUBJECT_IDS_2

    def get_subject_names(self):
        if self.grade_lev == 2:
            return Gradation.SUBJECT_NAMES_2

    def get_exam_ids(self):
        sql = """
            SELECT examId
            FROM qam_semester_info
            WHERE enrollYear = %d AND gradeLev = %d
            ORDER BY gradeId, xq, examType;
        """ % (self.enroll_year, self.grade_lev)
        return list_util.to_a_list(base_dao.select(sql))

    def get_exam_nicks(self):
        sql = """
            SELECT examNick
            FROM qam_semester_info
            WHERE enrollYear = %d AND gradeLev = %d
            ORDER BY gradeId, xq, examType;
        """ % (self.enroll_year, self.grade_lev)
        return list_util.to_a_list(base_dao.select(sql))

    def get_subject_start_exam_id(self, subject_id):
        sql = """
              SELECT examId
              FROM qam_semester_info
              WHERE enrollYear = %d AND gradeLev = %d AND examId IN
              (
                  SELECT DISTINCT examId
                  FROM qa_district_dimen
                  WHERE subjectId = %d
              )
              ORDER BY gradeId, xq, examType
              LIMIT 0, 1;
          """ % (self.enroll_year, self.grade_lev, subject_id)
        return base_dao.select_one_cell(sql)

    def get_subject_exam_start(self, subject_id):
        return self.get_exam_ids().index(self.get_subject_start_exam_id(subject_id))

    def get_subject_index(self, subject_id):
        return self.subject_ids.index(subject_id)

    def get_subject_name_by_id(self, subject_id):
        return self.subject_names[self.get_subject_index(subject_id)]


class Exam(object):
    SPECIAL = 1
    CURRENT = 2

    def __init__(self, gradation, exam_id, base_student):
        self.gradation = gradation
        # self.gradation = Gradation()
        self.exam_id = exam_id
        self.exam_nick = self.get_exam_nick()
        self.base_student = base_student
        self.school_table = table_config.get_school_sum_table(table_config.QA_CODE)
        if base_student == Exam.SPECIAL:
            self.class_table = table_config.get_class_sum_table(table_config.QA_ZK_CODE)
        elif base_student == Exam.CURRENT:
            self.class_table = table_config.get_class_sum_table(table_config.QA_CODE)

        self.school_ids = self.get_school_ids()
        self.school_names = self.get_school_names()
        self.school_types = self.get_school_types()
        self.class_ids = self.get_class_ids()
        self.class_names = self.get_class_names()

        self.exam_ids = []
        self.exam_nicks = []
        self.exam_diff_ids = []
        for subject_id in gradation.subject_ids:
            self.exam_ids.append(self.get_exam_ids(subject_id))
            self.exam_nicks.append(self.get_exam_nicks(subject_id))
            self.exam_diff_ids.append(self.get_exam_diff_ids(subject_id))

        self.distribution_ids = []
        self.distribution_names = []
        self.subject_distribution_type = []
        distribution = Distribution(self.exam_nick, "总分")
        self.count = distribution.get_count()

        self.subject_totals = []
        total = Total(self.exam_nick, "总分")
        self.subject_totals.append(total.get_total())

        self.subject_distribution_type.append(distribution.get_distributions()[0])
        self.distribution_ids.append(distribution.get_ids())
        self.distribution_names.append(distribution.get_names())
        for subject_name in gradation.subject_names:
            distribution.subject_name = subject_name
            self.distribution_ids.append(distribution.get_ids())
            self.subject_distribution_type.append(distribution.get_distributions()[0])
            self.distribution_names.append(distribution.get_names())
            self.subject_totals.append(total.get_total())

    def get_school_ids(self):
        return qam_dao.get_all_school_ids_order(self.gradation.grade_lev, self.exam_id, self.school_table)

    def get_school_names(self):
        return qam_dao.get_all_school_names_order(self.gradation.grade_lev, self.exam_id, self.school_table)

    def get_school_types(self):
        return qam_dao.get_all_school_types_order(self.gradation.grade_lev, self.exam_id, self.school_table)

    def get_class_ids(self):
        return qam_dao.get_all_school_class_ids(self.gradation.grade_lev, self.exam_id, self.class_table)

    def get_class_names(self):
        return qam_dao.get_all_school_class_names(self.gradation.grade_lev, self.exam_id, self.class_table)

    def get_exam_ids(self, subject_id):
        exam_ids = self.gradation.get_exam_ids()
        start = self.gradation.get_subject_exam_start(subject_id)
        end = exam_ids.index(self.exam_id)
        return exam_ids[start:end + 1]

    def get_exam_nicks(self, subject_id):
        exam_nicks = self.gradation.get_exam_nicks()
        start = self.gradation.get_subject_exam_start(subject_id)
        end = exam_nicks.index(self.exam_nick)
        return exam_nicks[start:end + 1]

    def get_exam_nick(self):
        sql = """
                SELECT examNick
                FROM qam_semester_info
                WHERE examId = '%s';
            """ % self.exam_id
        return base_dao.select_one_cell(sql)

    def get_exam_diff_ids(self, subject_id):
        exam_ids = self.get_subject_exam_ids(subject_id)
        length = len(exam_ids)

        result = []
        for index in range(length - 1):
            result.append([exam_ids[index], exam_ids[index + 1]])
        if length > 2:
            result.append([exam_ids[0], exam_ids[- 1]])
        return result

    def get_district_varied_ids(self, district_code):
        if district_code == Gradation.DISTRICT_CODE:
            return self.gradation.district_ids
        elif district_code == Gradation.SCHOOL_CODE:
            return self.school_ids
        elif district_code == Gradation.CLASS_CODE:
            return self.class_ids

    def get_subject_exam_ids(self, subject_id):
        return self.exam_ids[self.gradation.get_subject_index(subject_id)]

    def get_subject_exam_diff_ids(self, subject_id):
        return self.exam_diff_ids[self.gradation.get_subject_index(subject_id)]

    def get_subject_distribution_ids(self, subject_id=None):
        if subject_id is None:
            return self.distribution_ids[0]
        else:
            return self.distribution_ids[self.gradation.get_subject_index(subject_id) + 1]

    def get_subject_distribution_names(self, subject_id=None):
        if subject_id is None:
            return self.distribution_names[0]
        else:
            return self.distribution_names[self.gradation.get_subject_index(subject_id) + 1]

    def get_subject_distribution_type(self, subject_id=None):
        if subject_id is None:
            return self.subject_distribution_type[0]
        else:
            return self.subject_distribution_type[self.gradation.get_subject_index(subject_id) + 1]

    def get_subject_total(self, subject_id=None):
        if subject_id is None:
            return self.subject_totals[0]
        else:
            return self.subject_totals[self.gradation.get_subject_index(subject_id) + 1]

    def get_std_school_names(self, school_id):
        result = []
        for index, value in enumerate(self.school_ids):
            result.append("学校%d" % (index + 1))
        index = self.get_school_index(school_id)
        result[index] = self.school_names[index]
        return result

    def get_school_index(self, school_id):
        return self.school_ids.index(school_id)


class Range(object):
    def __init__(self, start=0, end=0, step=0):
        self.start = start
        self.end = end
        self.step = step

    def set_value(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def get_ids(self):
        ids = []
        scopes = range(self.start, self.end, self.step)
        for index, scope in enumerate(scopes[0:-1]):
            ids.append([scope, scopes[index + 1]])
        if scopes[-1] < self.end:
            ids.append([scopes[-1], self.end])
        return ids

    def get_names(self):
        names = []
        scopes = range(self.start, self.end, self.step)
        for index, scope in enumerate(scopes[0:-1]):
            names.append("(%d, %d]" % (scope, scopes[index + 1]))
        if scopes[-1] < self.end:
            names.append("(%d, %d]" % (scopes[-1], self.end))
        return names


class Distribution(object):
    ALL = 1
    SCORE = 2
    COUNT = 3

    DISTRIBUTION_SCORE_150 = [SCORE, [[0, 150, 5], ]]
    DISTRIBUTION_SCORE_100 = [SCORE, [[0, 100, 5], ]]
    DISTRIBUTION_SCORE_90 = [SCORE, [[0, 90, 5], ]]
    DISTRIBUTION_SCORE_60 = [SCORE, [[0, 60, 5], ]]
    DISTRIBUTION_COUNT_650_5 = [COUNT, [[0, 120, 120], [120, 650, 5], ], 5]
    DISTRIBUTION_COUNT_600_5 = [COUNT, [[0, 120, 120], [120, 600, 5], ], 5]

    SUBJECT_DISTRIBUTIONS = {
        "初三一模": {
            "语文": DISTRIBUTION_SCORE_150,
            "数学": DISTRIBUTION_SCORE_150,
            "英语": DISTRIBUTION_SCORE_150,
            "物理": DISTRIBUTION_SCORE_100,
            "化学": DISTRIBUTION_SCORE_100,
            "总分": DISTRIBUTION_COUNT_650_5,
        },
        "初三二模": {
            "语文": DISTRIBUTION_SCORE_150,
            "数学": DISTRIBUTION_SCORE_150,
            "英语": DISTRIBUTION_SCORE_150,
            "物理": DISTRIBUTION_SCORE_90,
            "化学": DISTRIBUTION_SCORE_60,
            "总分": DISTRIBUTION_COUNT_600_5,
        },
    }

    def __init__(self, exam_nick, subject_name):
        self.exam_nick = exam_nick
        self.subject_name = subject_name

    def get_distributions(self):
        return Distribution.SUBJECT_DISTRIBUTIONS[self.exam_nick][self.subject_name]

    def get_ids(self):
        ranges = self.get_distributions()[1]
        ids = []
        r = Range()
        for value in ranges:
            r.set_value(*value)
            ids.extend(r.get_ids())
        return ids

    def get_names(self):
        distributions = self.get_distributions()
        t = distributions[0]
        ranges = distributions[1]

        names = []
        r = Range()
        for value in ranges:
            r.set_value(*value)
            names.extend(r.get_names())

        if t == Distribution.ALL:
            start = ranges[0][0]
            step = ranges[0][2]
            names[0] = "[%d, %d]" % (start, start + step)
        return names

    def get_count(self):
        return Distribution.SUBJECT_DISTRIBUTIONS[self.exam_nick][self.subject_name][2]


class Total(object):
    SUBJECT_TOTAL = {
        "初三一模": {
            "语文": 150,
            "数学": 150,
            "英语": 150,
            "物理": 100,
            "化学": 100,
            "总分": 650,
        },
        "初三二模": {
            "语文": 150,
            "数学": 150,
            "英语": 150,
            "物理": 90,
            "化学": 60,
            "总分": 600,
        },
    }

    def __init__(self, exam_nick, subject_name):
        self.exam_nick = exam_nick
        self.subject_name = subject_name

    def get_total(self):
        return Total.SUBJECT_TOTAL[self.exam_nick][self.subject_name]


class Where(object):
    DISTRICT_CODE = 1
    SCHOOL_CODE = 2
    CLASS_CODE = 3

    def __init__(self, exam_id):
        self.fixed_exam = qa.Where("examId", exam_id)

        self.varied_exam = qa.Where("examId")
        self.district = qa.Where("districtId")
        self.school = qa.Where("schoolId")
        self.subject = qa.Where("subjectId")
        self.class_t = qa.Where('classId')

        self.greater = qa.Where("sum", symbol=">")
        self.less_equal = qa.Where("sum", symbol="<=")
        self.greater_equal = qa.Where("sum", symbol=">=")
        self.count = qa.Where("count")

        self.font_exam = qa.Where("font.examId")
        self.behind_exam = qa.Where("behind.examId")
        self.font_school = qa.Where("font.schoolId")
        self.behind_school = qa.Where("behind.schoolId")
        self.font_subject = qa.Where("font.subjectId")
        self.behind_subject = qa.Where("behind.subjectId")

    def get_varied_district(self, district_code):
        if district_code == Where.DISTRICT_CODE:
            return self.district
        elif district_code == Where.SCHOOL_CODE:
            return self.school
        elif district_code == Where.CLASS_CODE:
            return [self.school, self.class_t]

    def get_varied_greater_less_equal(self):
        return [self.greater, self.less_equal]

    def get_varied_greater_equal_less_equal(self):
        return [self.greater_equal, self.less_equal]

    def get_varied_exam_diff(self):
        return [self.font_exam, self.behind_exam]

    def get_varied_exam(self):
        return self.varied_exam

    def get_fixed_exam(self):
        return self.fixed_exam

    def get_fixed_subject(self, subject_id):
        self.subject.set_value(subject_id)
        return self.subject

    def get_fixed_district(self, district_code, value):
        result = self.get_varied_district(district_code)
        qa.CellWhere.set_value_static(result, value)
        return result

    def get_fixed_district_subject(self, district_code, value, subject_id=None):
        result = self.get_fixed_district(district_code, value)
        if subject_id is None:
            return result

        if district_code == Where.CLASS_CODE:
            result.append(self.get_fixed_subject(subject_id))
            return result
        else:
            return [result, self.get_fixed_subject(subject_id)]

    def get_fixed_exam_subject(self, subject_id=None):
        result = self.fixed_exam
        if subject_id is None:
            return result

        return [result, self.get_fixed_subject(subject_id)]

    def get_fixed_diff_school_subject(self, school_id, subject_id):
        self.font_school.set_value(school_id)
        self.font_subject.set_value(subject_id)
        self.behind_school.set_value(school_id)
        self.behind_subject.set_value(subject_id)
        return [self.font_school, self.font_subject, self.behind_school,
                self.behind_subject]

    def get_exam_count_fixed_where(self, count):
        self.count.set_value(count)
        return [self.fixed_exam, self.count]


if __name__ == '__main__':
    d1 = datetime.datetime.now()
    enroll_year = 2014
    grade_lev = 2
    gradation = Gradation(enroll_year, grade_lev)

    exam_id = '8c4646637f44489c9ba9333e580fe9d0'
    base_student = Exam.SPECIAL
    exam = Exam(gradation, exam_id, base_student)
    d2 = datetime.datetime.now()
    print(d2 - d1)
