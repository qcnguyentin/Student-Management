from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from Stud_Man import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    TEACHER = 1
    EMPLOYEE = 2
    ADMIN = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole))

    regulation = relationship('Regulation', backref=backref('user'))

    teacher_class = relationship('TeacherClass', backref=backref('user'), lazy=True)

    user_semester = relationship('UserSemester', backref=backref('user'), lazy=True)

    user_subject = relationship('UserSubject', backref=backref('user'), lazy=True)

    def __str__(self):
        return self.name


class Regulation(BaseModel):
    type_regulation = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    # def __str__(self):
    #     return self.user_id


class MyClass(BaseModel):
    name = Column(String(20), nullable=False)
    teacher_class = relationship('TeacherClass', backref=backref('my_class'), lazy=True)
    student_class = relationship('StudentClass', backref=backref('my_class'), lazy=True)
    score = relationship('Score', backref=backref('my_class'), lazy=True)

    def __str__(self):
        return self.name


class Student(BaseModel):
    name = Column(String(50), nullable=False)
    sex = Column(String(20), nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100))
    student_class = relationship('StudentClass', backref=backref('student'), lazy=True)
    student_semester = relationship('StudentSemester', backref=backref('student'), lazy=True)
    score = relationship('Score', backref=backref('student'), lazy=True)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    semester = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    student_semester = relationship('StudentSemester', backref=backref('semester'), lazy=True)
    user_semester = relationship('UserSemester', backref=backref('semester'), lazy=True)
    score = relationship('Score', backref=backref('semester'), lazy=True)


class Subject(BaseModel):
    name = Column(String(50), nullable=False)
    score = relationship('Score', backref=backref('subject'), lazy=True)
    user_subject = relationship('UserSubject', backref=backref('subject'), lazy=True)

    def __str__(self):
        return self.name


class Score(BaseModel):
    score = Column(Float, nullable=False)
    type_score = Column(String(20), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    class_id = Column(Integer, ForeignKey(MyClass.id), nullable=False)


class TeacherClass(BaseModel):
    date = Column(DateTime, default=datetime.now())
    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)
    class_id = Column(Integer, ForeignKey(MyClass.id), nullable=False)


class StudentClass(BaseModel):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    class_id = Column(Integer, ForeignKey(MyClass.id), nullable=False)


class StudentSemester(BaseModel):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)


class UserSemester(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)


class UserSubject(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # import hashlib
        #
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        #
        # # u = User(name='Nguyễn Văn A', username='teacher6', password=password, user_role=UserRole.TEACHER,
        # #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # u1 = User(name='Trần Thị B', username='teacher7', password=password, user_role=UserRole.TEACHER,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # u2 = User(name='Võ Văn C', username='teacher8', password=password, user_role=UserRole.TEACHER,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add_all([u1, u2])
        # db.session.commit()
