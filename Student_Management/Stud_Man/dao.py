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


def class_name():
    return MyClass.query.all()


def subject():
    return Subject.query.all()


def semester():
    return Semester.query.group_by(Semester.year).all()


def student_id(keyword):
    query = MyClass.query.all()
    for s in query:
        if keyword:
            if s.name.contains(keyword):
                return s.id
    return None


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

    return query.all()


def load_class(class_id=None, kw=None):
    query = MyClass.query.filter(MyClass.active.__eq__(True))

    if class_id:
        query = query.filter(MyClass.id.__eq__(class_id))

    if kw:
        query = query.filter(MyClass.name.contains(kw))

    return query.all()


def save_score():
    pass


if __name__ == '__main__':
    with app.app_context():
        rep3 = student_score()
        print(rep3)
