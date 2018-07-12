class DistrictInfo(object):
    def __init__(self):
        self.district_id = ''
        self.district_name = ''


class SchoolInfo(DistrictInfo):
    def __init__(self):
        super(SchoolInfo, self).__init__()
        self.school_id = ''
        self.school_name = ''


class ClassInfo(SchoolInfo):
    def __init__(self):
        super(ClassInfo, self).__init__()
        self.class_id = ''
        self.class_name = ''


class SubjectInfo(object):
    def __init__(self):
        self.subject_id = 0
        self.subject_name = ''


class ExamInfo(object):

    def __init__(self, exam_id='', exam_nick='', enroll_year=0, grade_lev=0):
        self.exam_id = exam_id
        self.exam_nick = exam_nick
        self.enroll_year = enroll_year
        self.grade_lev = grade_lev

    def __repr__(self):
        return "enrollYear=" + str(self.enroll_year) + ", gradeLev=" + str(self.grade_lev) + \
               ", examNick=" + self.exam_nick + ", examId=" + self.exam_id


class DimenInfo(object):
    def __init__(self):
        self.dimen_descriptin = ''
        self.number = 0


if __name__ == '__main__':
    school_info = SchoolInfo()
    print(school_info.school_name)

    class_info = ClassInfo()
    print(class_info.school_id)
    print(class_info.school_name)

    exam_info1 = ExamInfo()
    exam_info2 = ExamInfo()

    if hasattr(exam_info1, "enroll_year"):
        setattr(exam_info1, "enroll_year", 2014)
    ExamInfo.enroll_year = 2018
    print(exam_info1.enroll_year)
    print(exam_info2.enroll_year)
    print(ExamInfo.enroll_year)
