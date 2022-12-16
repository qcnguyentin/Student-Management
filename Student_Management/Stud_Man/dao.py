import hashlib

from flask import jsonify
from pymysql import *
from Stud_Man import app, db, utils
from flask_login import current_user
from sqlalchemy import func
import hashlib
from Stud_Man.models import User, UserRole, MyClass, UserSubject, UserSemester, StudentSemester, Subject, \
    TeacherClass, Student, Semester, Regulation, StudentClass, Score
from datetime import datetime


#lấy user bằng id
def get_user_by_id(user_id):
    return User.query.get(user_id)


#xác thực user
def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

# lấy ngày phụ trách, tên lớp, sĩ số (class, teacher_class)
# lấy tên giáo viên
#lấy ra các giá trị để hiện thông tin giáo viên nhận lớp nào thời gian nào
def teach_class(kw=None):
    query = db.session.query(MyClass.name, User.name, TeacherClass.date) \
        .join(MyClass, TeacherClass.class_id.__eq__(MyClass.id)) \
        .join(User, TeacherClass.teacher_id.__eq__(User.id)) \
        .order_by(MyClass.name)

    if kw:
        query = query.filter(MyClass.name.contains(kw))

    return query.all()


#lấy danh sách điểm
def student_score():
    return Score.query.all()


#lấy danh sách môn học
def subject():
    return Subject.query.all()


#lấy danh sách học kỳ
def semester():
    return Semester.query.group_by(Semester.year).all()


#lấy danh sách lớp
def my_class():
    return MyClass.query.all()


#kiểm tra học sinh có học lớp chỉ định và có học trong học kỳ đó không để thêm điểm
def check_student_class_semester(student_id=None, class_name=None, year=None):
    query = db.session.query(Student.id, MyClass.name, Semester.semester, Semester.year, MyClass.id) \
        .join(StudentClass, Student.id.__eq__(StudentClass.student_id)) \
        .join(MyClass, StudentClass.class_id.__eq__(MyClass.id)).all()
    check = False

    if student_id and class_name and year:
        for s in query:
            if s[0] == student_id and s[1] == class_name and s[3] == int(year):
                check = True
    return check


#xóa điểm
def delete_score(score_id):
    score = Score.query

    if score_id:
        score = score.filter(Score.id.__eq__(score_id)).delete()
        db.session.commit()
        return True
    return False


#cập nhật điểm
def update_score(score_id, score_value):
    score = Score.query
    if score_id:
        score = score.filter(Score.id.__eq__(score_id)).first()
        score.score = float(score_value)
        db.session.add(score)
        db.session.commit()
        return True
    return False


#lấy học sinh từ id
def get_student_by_id(student_id):
    return Student.query.get(student_id)


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

    return query.all()


#lấy danh sách học sinh
def load_class(class_id=None, kw=None):
    query = MyClass.query

    if class_id:
        query = query.filter(MyClass.id.__eq__(class_id))

    if kw:
        query = query.filter(MyClass.name.contains(kw))

    return query.all()


#kiểm tra điểm thuộc loại nào của học sinh nào học kỳ nào đã vượt số lượng cho phép chưa để thêm điểm
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


#lưu điểm sau khi thêm
def save_score(student_id, score, type_score, class_name, semester, subject_name, year):
    query = Student.query.filter(Student.id.__eq__(student_id))
    for i in query:
        query = i.name
    score = check_max_score(query, score, type_score, class_name, semester, subject_name, year)
    if score:
        db.session.add(score)
        db.session.commit()
        return score
    return "Lưu không thành công"


#lấy các giá trị để tính trung bình trong năm học để xuất bảng điểm
def score_average(year):
    query = "SELECT my_class.name, score.score, semester.semester, semester.year, student.name, score.type_score, student.id, subject.name FROM `std-mana`.my_class, `std-mana`.score, `std-mana`.semester, student, subject WHERE my_class.id = score.class_id and score.semester_id = semester.id and score.student_id = student.id and subject.id = score.subject_id and semester.year = {}".format(
        year)
    df = db.session.execute(query).all()
    return df


#lấy học sinh
def student():
    return Student.query.all()


#thêm học sinh
def add_student(student_name, student_sex, student_dob, student_address, student_email, student_phone):
    if student_name and student_sex and student_dob and student_address:
        student = Student(name=student_name, sex=student_sex, dob=student_dob, address=student_address,
                          phone=student_phone, email=student_email)
        db.session.add(student)
        db.session.commit()
    return Student.query.all()


#kiểm tra độ tuổi có đúng quy định không
def check_age(student_dob):
    dt = datetime.strptime(student_dob, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dt.year
    min_age = Regulation.query.filter(Regulation.type_regulation.__eq__("Tuôi tối thiểu")).all()
    max_age = Regulation.query.filter(Regulation.type_regulation.__eq__("Tuôi tối đa")).all()
    for s in min_age:
        min_age = s.size
    for s in max_age:
        max_age = s.size
    if min_age <= age <= max_age:
        return True
    return False


#cập nhật thông tin học sinh
def update_student(student_id, student_name, student_dob, student_address, student_phone, student_mail):
    std = Student.query
    if student_id:
        std = std.filter(Student.id.__eq__(int(student_id))).first()
        std.name = student_name
        std.dob = student_dob
        std.address = student_address
        std.phone = student_phone
        std.mail = student_mail
        db.session.add(std)
        db.session.commit()
        return True
    return False


#duyệt ds học sinh
def student_search_to_list(student_name=None, student_mshs=None):
    query = Student.query

    if student_name:
        query = query.filter(Student.name.contains(student_name))

    if student_mshs:
        query = query.filter(Student.id.__eq__(student_mshs))

    return query.all()


#đếm sĩ số lớp
def count_student_by_class():
    query = "SELECT my_class.id, my_class.name, count(student.id), semester.year, semester.semester FROM student, my_class, student_class, student_semester, semester WHERE student.id = student_class.student_id and student_class.class_id = my_class.id and student.id = student_semester.student_id and student_semester.semester_id = semester.id group by my_class.id, semester.year, semester.semester order by my_class.id"
    df = db.session.execute(query).all()
    year = datetime.now().year
    stats = []
    for s in df:
        if s[3] == year and s[4] == 1:
            stats.append(s)
    return stats


#tính điểm trung bình 1 môn chỉ định
def cal_avg_sj(data):
    score = []
    student_id_list = []
    count = []
    my_class = []
    for s in data:
        if s['class'] not in my_class:
            my_class.append(s['class'])
    for s in data:
        if s['student_id'] not in student_id_list:
            student_id_list.append(s['student_id'])
            score.append(0)
            count.append(0)
    for s in range(len(student_id_list)):
        for c in range(len(data)):
            if data[c]['student_id'] == student_id_list[s] and data[c]['class'] == my_class[0]:
                if data[c]['type_score'] == "Điểm 1 tiết":
                    score[s] += 2 * data[c]['score']
                    count[s] += 2
                elif data[c]['type_score'] == "Điểm 15p":
                    score[s] += data[c]['score']
                    count[s] += 1
                else:
                    score[s] += 3 * data[c]['score']
                    count[s] += 3
    score_avg = []
    for i in range(len(count)):
        if count[i] == 0:
            count[i] = 1
    for i in range(len(score)):
        score_avg.append(score[i]/count[i])
    return score_avg


#kiểm tra số lượng học sinh qua 1 môn chỉ định của 1 lớp
def stats_pass_subject(kw=None, subject=None, semester=None, class_name=None):
    std_cls = StudentClass.query.all()
    sc = Score.query.all()
    score_list = []
    if not semester:
        semester = 0
    for s in sc:
        for std in std_cls:
            if s.student_id == std.student_id and s.semester.semester == int(semester) and s.subject.name == subject and s.my_class.name == class_name:
                score_list.append({
                    'student_id': s.student_id,
                    'score': s.score,
                    'type_score': s.type_score,
                    'class': std.my_class.name
                })
                break
    std_pass = []
    score = cal_avg_sj(score_list)
    student_id_list = []
    status = []
    size_of_class = 0
    pass_sj = 0
    for i in score:
        if i >= 5:
            status.append(True)
        else:
            status.append(False)
    for s in score_list:
        if s['student_id'] not in student_id_list and s['class'] == class_name:
            student_id_list.append(s['student_id'])
            size_of_class += 1
            for j in sc:
                for std in std_cls:
                    if j.student_id == std.student_id and j.semester.semester == int(
                            semester) and j.subject.name == subject and j.my_class.name == class_name:
                        score_list.append({
                            'student_id': j.student_id,
                            'score': j.score,
                            'type_score': j.type_score,
                            'class': std.my_class.name
                        })
                        break
    for i in range(len(student_id_list)):
        std_pass.append({
            "student_id": student_id_list[i],
            "score_avg": score[i],
            "status_pass": status[i],
        })
    for i in range(len(std_pass)):
        if student_id_list[i] == std_pass[i]["student_id"]:
            if std_pass[i]["status_pass"]:
                pass_sj += 1
    if size_of_class == 0:
        size_of_class = 1
    percent = pass_sj * 100/size_of_class
    stt = 0
    return {
        'size_of_class': size_of_class,
        'pass_sj': pass_sj,
        'percent': round(percent, 2),
        "class_name": class_name
    }


#kiểm tra số lượng học sinh qua 1 môn chỉ định của các lớp
def mutil_class_pass(kw=None, subject=None, semester=None):
    class_name = MyClass.query.all()
    list_pass = []
    stt = 0
    for s in class_name:
        stt += 1
        list_pass.append({
            'stt': stt,
            'pass': stats_pass_subject(kw, subject, semester, s.name)
        })
    return list_pass


def check_max_student():
    query = Regulation.query.all()
    for i in query:
        if i.type_regulation == "Sĩ số lớp":
            return i.size


def save_class_list(class_name, student_list):
    my_cl = my_class()
    st = StudentClass.query.all()
    flag = False
    if class_name:
        for i in my_cl:
            if class_name == i.name:
                my_cl = i
                flag = True
                break
        if not flag:
            my_cl = MyClass(name=class_name)
            db.session.add(my_cl)
            flag = True
        for s in student_list:
            if flag:
                for i in st:
                    if i.student_id == int(s) and i.my_class.name == class_name:
                        return {
                            'student_id': s,
                            'class_name': class_name
                        }
                    else:
                        stud_cl = StudentClass(my_class=my_cl, student_id=int(s))
                        db.session.add(stud_cl)
                        try:
                            db.session.commit()
                        except:
                            return False
                        else:
                            return True
    else:
        return False