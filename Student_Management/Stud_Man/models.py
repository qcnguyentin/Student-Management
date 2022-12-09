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
    from_age = Column(Integer, nullable=False)
    to_age = Column(Integer, nullable=False)
    size_of_class = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    # def __str__(self):
    #     return self.user_id


class Class(BaseModel):
    name = Column(String(20), nullable=False)
    teacher_class = relationship('TeacherClass', backref=backref('class'), lazy=True)
    student_class = relationship('StudentClass', backref=backref('class'), lazy=True)
    score = relationship('Score', backref=backref('class'), lazy=True)

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
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)


class TeacherClass(BaseModel):
    date = Column(DateTime, default=datetime.now())
    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)


class StudentClass(BaseModel):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)


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


        # cls1 = Class(name='11A1', size=33)
        # cls2 = Class(name='12A1', size=40)
        # cls3 = Class(name='10A2', size=25)
        # db.session.add_all([cls1, cls2, cls3])
        # db.session.commit()

        #
        # r1 = Regulation(content='Mặc áo trắng sơ mi, quần tây đen', user_id=1)
        # db.session.add(r1)
        # db.session.commit()
        #
        #
        # std1 = Student(name='Đặng Thái E', sex='Nữ', dob=datetime.now(), address='Phú Yên')
        # std2 = Student(name='Nguyễn Thái F', sex='Nam', dob=datetime.now(), address='Phú Yên')
        # std3 = Student(name='Nguyễn Thị G', sex='Nữ', dob=datetime.now(), address='Phú Yên')
        # db.session.add_all([std1, std2, std3])
        # db.session.commit()
        #
        # smt1 = Semester(semester=1, year=2020)
        # db.session.add(smt1)
        # db.session.commit()

        # sj1 = Subject(name='Toán')
        # sj2 = Subject(name='Lý')
        # sj3 = Subject(name='Hóa')
        # sj4 = Subject(name='Văn')
        # db.session.add_all([sj1, sj2, sj3, sj4])
        # db.session.commit()

        # sc1 = Score(score=9, type_score=1, student_id=1, subject_id=1)
        # sc2 = Score(score=10, type_score='15 phút', student_id=2, subject_id=2)
        # sc3 = Score(score=10, type_score='Cuối kỳ', student_id=3, subject_id=1)
        # sc4 = Score(score=8, type_score='1 tiết', student_id=4, subject_id=3)
        # sc5 = Score(score=7, type_score='15 phút', student_id=5, subject_id=4)
        # sc6 = Score(score=9, type_score='15 phút', student_id=6, subject_id=5)
        # sc7 = Score(score=8, type_score='1 tiết', student_id=7, subject_id=6)
        #
        # db.session.add_all([sc1, sc2, sc3, sc4, sc5, sc6, sc7])
        # db.session.commit()

        # t_c1 = TeacherClass("2022-12-4", 10, 6)
        # db.session.add(t_c1)
        # db.session.commit()

        # s_c1 = StudentClass(student_id=1, class_id=1)
        # s_c2 = StudentClass(student_id=2, class_id=3)
        # db.session.add_all([s_c1, s_c2])
        # db.session.commit()

        # s_s1 = student_semester(student_id=1, semester_id=1)
        # db.session.add(s_s1)
        # db.session.commit()
        #
        # u_s1 = user_semester(user_id=2, semester_id=1)
        # db.session.add(u_s1)
        # db.session.commit()

        # u_sj1 = U(user_id=1, subject_id=1)
        # db.session.add(u_sj1)
        # db.session.commit()
