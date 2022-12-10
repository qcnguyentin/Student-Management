import hashlib
from Stud_Man import app, db
from flask_login import current_user
from sqlalchemy import func
import hashlib
from Stud_Man.models import User, UserRole, MyClass, UserSubject, UserSemester, StudentSemester, Subject, \
    TeacherClass, Student, Semester, Regulation, StudentClass, Score


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

    # lấy ngày phụ trách, tên lớp, sĩ số (class, teacher_class)
    # lấy tên giáo viên


def teach_class(kw=None):
    query = db.session.query(MyClass.name, User.name, TeacherClass.date) \
        .join(MyClass, TeacherClass.class_id.__eq__(MyClass.id)) \
        .join(User, TeacherClass.teacher_id.__eq__(User.id)) \
        .order_by(MyClass.name)

    if kw:
        query = query.filter(MyClass.name.contains(kw))

    return query.all()


def student_score():
    return Score.query.all()


def student():
    return Student.query.all()


def subject():
    return Subject.query.all()


def semester():
    return Semester.query.group_by(Semester.year).all()


def my_class():
    return MyClass.query.all()


def check_student_class_semester(student_name=None, class_name=None, semester=None, year=None):
    query = db.session.query(Student.name, MyClass.name, Semester.semester, Semester.year, MyClass.id) \
        .join(StudentClass, Student.id.__eq__(StudentClass.student_id)) \
        .join(MyClass, StudentClass.class_id.__eq__(MyClass.id)) \
        .join(StudentSemester, Student.id.__eq__(StudentSemester.student_id)) \
        .join(Semester, StudentSemester.semester_id.__eq__(Semester.id)).all()
    check = False

    if student_name and class_name and semester and year:
        for s in query:
            if s[0] == student_name and s[1] == class_name and s[2] == int(semester) and s[3] == int(year):
                check = True
    return check



# tìm kiếm học sinh
def student_search(student_name=None, student_class=None, student_mshs=None):
    query = db.session.query(Student.id, Student.name, MyClass.name, Student.sex, Student.dob, Student.address,
                             Student.email) \
        .join(StudentClass, Student.id.__eq__(StudentClass.student_id)) \
        .join(MyClass, StudentClass.class_id.__eq__(MyClass.id)) \
        .order_by(Student.id)

    if student_name:
        query = query.filter(Student.name.contains(student_name))

    if student_class:
        query = query.filter(MyClass.name.contains(student_class))

    if student_mshs:
        query = query.filter(Student.id.contains(student_mshs))
        print(query)

    return query.all()


def load_class(class_id=None, kw=None):
    query = MyClass.query

    if class_id:
        query = query.filter(MyClass.id.__eq__(class_id))

    if kw:
        query = query.filter(MyClass.name.contains(kw))

    return query.all()


def check_max_score(student_name, score, type_score, class_name, semester, subject_name, year):
    # lấy dữ liệu so sánh với điểm cần thêm
    student_name = Student.query.filter(Student.name.__eq__(student_name)).all()
    subject_name = Subject.query.filter(Subject.name.__eq__(subject_name)).all()
    class_name = MyClass.query.filter(MyClass.name.__eq__(class_name)).all()
    semester_id = Semester.query.filter(
        Semester.semester.__eq__(int(semester))).filter(
        Semester.year.__eq__(int(year))).all()

    # biến lưu giá trị id gán vào score
    stud_id = 0
    subject_id = 0
    class_id = 0

    # vòng lặp lấy id
    for a in student_name:
        stud_id = a.id
    for a in subject_name:
        subject_id = a.id
    for a in class_name:
        class_id = a.id
    for a in semester_id:
        semester_id = a.id

    # biến lưu giá trị đã lấy từ web
    score = Score(score=int(score), type_score=type_score, student_id=stud_id, subject_id=subject_id,
                  semester_id=semester_id, class_id=class_id)

    # biến để đếm số lượng các điểm đã vượt mức chưa
    score_student = Score.query.filter(Score.student_id.__eq__(stud_id)).filter(Score.class_id.__eq__(class_id)).filter(
        Score.semester_id.__eq__(semester_id)).filter(Score.subject_id.__eq__(subject_id)).all()
    print(score_student)
    count_max_score = 0
    # bảng relugation có lưu giá trị quy định điểm tối đa
    max_15m = Regulation.query.filter(Regulation.type_regulation.__eq__("Số điểm 15p")).all()
    max_45m = Regulation.query.filter(Regulation.type_regulation.__eq__("Số điểm 45p")).all()
    max_final_score = Regulation.query.filter(Regulation.type_regulation.__eq__("Số điểm thi")).all()
    for s in max_15m:
        max_15m = s.size
    for s in max_45m:
        max_45m = s.size
    for s in max_final_score:
        max_final_score = s.size
    for s in score_student:
        count_max_score += 1
    # kiểm tra số điểm đã vượt chưa
    if (type_score == 'Điểm 15p' and count_max_score < max_15m) or (
            type_score == 'Điểm 1 tiết' and count_max_score < max_45m) or (
            type_score == 'Điểm thi' and count_max_score < max_final_score):
        return score
    return False


def save_score(student_name, score, type_score, class_name, semester, subject_name, year):
    score = check_max_score(student_name, score, type_score, class_name, semester, subject_name, year)
    if score:
        print(score.student_id)
        db.session.add(score)
        db.session.commit()
        return score
    return "Lưu không thành công"


if __name__ == '__main__':
    with app.app_context():
        rep = check_student_class_semester("Đặng Thị S", "10A1", 2, 2022)
        print(rep)
