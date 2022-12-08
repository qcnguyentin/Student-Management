import hashlib
from Stud_Man import app, db
from flask_login import current_user
from sqlalchemy import func
import hashlib
from Stud_Man.models import User, UserRole, Class, UserSubject, UserSemester, StudentSemester, Subject, \
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
    query = db.session.query(Class.name, User.name, Class.size, TeacherClass.date) \
        .join(Class, TeacherClass.class_id.__eq__(Class.id)) \
        .join(User, TeacherClass.teacher_id.__eq__(User.id)) \
        .order_by(Class.name)

    if kw:
        query = query.filter(Class.name.contains(kw))

    return query.all()


def student_score(kw=None):
    query = db.session.query(Student.name, Score.score, Score.id, Score.type_score, Class.name, Subject.name,
                             Semester.semester, Semester.year) \
        .join(Student, Score.student_id.__eq__(Student.id)) \
        .join(StudentClass, Student.id.__eq__(StudentClass.student_id)) \
        .join(Class, StudentClass.class_id.__eq__(Class.id)) \
        .join(Subject, Score.subject_id.__eq__(Subject.id)) \
        .join(Semester, Score.semester_id.__eq__(Semester.id)) \
        .group_by(Student.name, Score.id).order_by(Score.id)

    if kw:
        query = query.filter(Class.name.contains(kw))

    return query.all()


def select_student():
    return db.session.query(Student.id, Student.name).all()


def select_class():
    return db.session.query(Class.id, Class.name).all()


def select_semester():
    return db.session.query(Semester.id, Semester.semester, Semester.year).group_by(Semester.year).all()


def student_search(student_name=None, student_class=None, student_mshs=None):
    query = db.session.query(Student.id, Student.name, Class.name, Student.sex, Student.dob, Student.address,
                             Student.email) \
        .join(StudentClass, Student.id.__eq__(StudentClass.student_id)) \
        .join(Class, StudentClass.class_id.__eq__(Class.id)) \
        .order_by(Student.id)

    if student_name:
        query = query.filter(Student.name.contains(student_name))

    if student_class:
        query = query.filter(Class.name.contains(student_class))

    if student_mshs:
        query = query.filter(Student.id.contains(student_mshs))

    return query.all()


# def check_age():
#
def load_class(class_id=None, kw=None):
    query = Class.query.filter(Class.active.__eq__(True))

    if class_id:
        query = query.filter(Class.id.__eq__(class_id))

    if kw:
        query = query.filter(Class.name.contains(kw))

    return query.all()


def save_score():
    pass


if __name__ == '__main__':
    with app.app_context():
        rep = student_score("10")
        print(rep)
        s = select_semester()
        print(s)
