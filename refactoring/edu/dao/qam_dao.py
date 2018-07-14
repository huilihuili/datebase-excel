import refactoring.edu.dao.base_dao as base_dao
import refactoring.edu.domain.qam as qam
import refactoring.edu.domain.qa as qa
import refactoring.edu.util.object_util as object_util
import refactoring.edu.config.item_config as item_config
import refactoring.edu.util.list_util as list_util


class Info(object):
    def get_all_info(self):
        return []

    def get_all_info_attr(self, *attr):
        return object_util.get_object_attrs(self.get_all_info(), *attr)


class DistrictInfo(Info):
    def get_all_info(self):
        sql = """
            SELECT districtId, districtName
            FROM qam_district_info;
        """
        return base_dao.select_with_object(sql, qam.DistrictInfo())


class SchoolInfo(Info):
    def __init__(self, grade_lev):
        self.grade_lev = grade_lev

    def get_all_info(self):
        sql = """
            SELECT schoolId, schoolName, xxbbm as districtId
            FROM qam_school_info
            WHERE gradeLev = %d;
        """ % self.grade_lev
        return base_dao.select_with_object(sql, qam.SchoolInfo())


class SchoolWithOrderInfo(SchoolInfo):
    def __init__(self, grade_lev, exam_id, table_name):
        super(SchoolWithOrderInfo, self).__init__(grade_lev)
        self.exam_id = exam_id
        self.table_name = table_name

    def get_all_info(self):
        sql = """
            SELECT info.schoolId, schoolName, xxbbm as districtId
            FROM %s AS school, qam_school_info AS info
            WHERE examId = '%s' AND gradeLev = %d AND school.schoolId = info.schoolId
            ORDER BY rank;
        """ % (self.table_name, self.exam_id, self.grade_lev)
        return base_dao.select_with_object(sql, qam.SchoolInfo())


class ClassWithOrderInfo(SchoolWithOrderInfo):
    def __init__(self, grade_lev, exam_id, table_name):
        super(ClassWithOrderInfo, self).__init__(grade_lev, exam_id, table_name)

    def get_all_info(self):
        sql = """
               SELECT schoolName, class.schoolId AS schoolId, className, classId 
               FROM %s AS class, qam_school_info AS info
               WHERE examId = '%s' AND gradeLev = %d AND class.schoolId = info.schoolId and classId IS NOT NULL
               ORDER BY rank;
           """ % (self.table_name, self.exam_id, self.grade_lev)
        return base_dao.select_with_object(sql, qam.ClassInfo())


def get_all_district_ids():
    return DistrictInfo().get_all_info_attr("district_id")


def get_all_district_names():
    return DistrictInfo().get_all_info_attr("district_name")


def get_all_school_ids(grade_lev):
    return SchoolInfo(grade_lev).get_all_info_attr("school_id")


def get_all_school_names(grade_lev):
    return SchoolInfo(grade_lev).get_all_info_attr("school_name")


def get_all_school_ids_order(grade_lev, exam_id, table_name):
    return SchoolWithOrderInfo(grade_lev, exam_id, table_name).get_all_info_attr("school_id")


def get_all_school_names_order(grade_lev, exam_id, table_name):
    return SchoolWithOrderInfo(grade_lev, exam_id, table_name).get_all_info_attr("school_name")


def get_all_school_types_order(grade_lev, exam_id, table_name):
    return SchoolWithOrderInfo(grade_lev, exam_id, table_name).get_all_info_attr("district_id")


def get_all_school_class_names(grade_lev, exam_id, table_name):
    return ClassWithOrderInfo(grade_lev, exam_id, table_name).get_all_info_attr("school_name", "class_name")


def get_all_school_class_ids(grade_lev, exam_id, table_name):
    return ClassWithOrderInfo(grade_lev, exam_id, table_name).get_all_info_attr("school_id", "class_id")


def get_exam_by_id(exam_id):
    sql = """
        SELECT enrollYear, gradeLev, examNick
        FROM qam_semester_info
        WHERE examId = '8c4646637f44489c9ba9333e580fe9d0';
    """
    exam = qam.ExamInfo(exam_id=exam_id)
    exam.enroll_year, exam.grade_lev, exam.exam_nick = base_dao.select_one_row(sql)
    return exam


def get_exam_ids(enroll_year, grade_lev):
    sql = """
        SELECT examId
        FROM qam_semester_info
        WHERE enrollYear = %d AND gradeLev = %d
        ORDER BY gradeId, xq, examType;
    """ % (enroll_year, grade_lev)
    return list_util.to_a_list(base_dao.select(sql))


def get_dimen_description_by_exam(exam_id, subject_id):
    where_list = qa.CellWhere(qa.Where("examId", exam_id), qa.Where("subjectId", subject_id))
    cell = qa.Cell(item_config.DIMEN_DESC_ITEMS, "qam_dimen_info", where_list)

    values = cell.get_row_values()
    values.reverse()
    for index, value in enumerate(values):
        if value is not None and value != '':
            result = values[index:]
            result.reverse()
            return result


def get_dimen_description_by_exams(exam_ids, subject_id):
    result = get_dimen_description_by_exam(exam_ids[0], subject_id)
    for exam_id in exam_ids[1:]:
        temp = get_dimen_description_by_exam(exam_id, subject_id)
        if len(result) > len(temp):
            result = temp
    return result


if __name__ == '__main__':
    print(get_dimen_description_by_exam("8c4646637f44489c9ba9333e580fe9d0", 121))
    print(get_dimen_description_by_exams(
        ['3f2a81437b944569aacb675a6544b2f3', '7c5315bb7c7a4cdb854d2893bfaebce5', '661cb10d97ae48c4a7207f1da9f6acdd',
         '8c4646637f44489c9ba9333e580fe9d0'], 121))
