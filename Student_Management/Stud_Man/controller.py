from datetime import datetime

import flask_login
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.functions import current_user
from Stud_Man import app, admin, login, controller, utils
from flask import render_template, redirect, request, session, jsonify
import dao
from Stud_Man.decorators import anonymous_user
from Stud_Man.utils import *


def index():
    user_role = check_user_role()
    rep = dao.teach_class(kw=request.args.get('keyword'))
    return render_template('index.html', rep=rep, user_role=user_role)


def search_student():
    kw = request.args.get('keyword')
    if kw:
        kw = kw
    else:
        kw = ''
    user_role = check_user_role()
    name = dao.student_search(student_name=request.args.get('student-name'),
                              student_class=request.args.get('student-class'),
                              student_mshs=request.args.get('student-mshs'))
    return render_template('search_student.html', name=name, user_role=user_role, kw=kw)


def score_manage():
    user_role = check_user_role()
    rep = dao.student_score()
    my_class = dao.my_class()
    semester = dao.semester()
    class_name = request.args.get('class-name')
    if class_name:
        class_name = class_name
    else:
        class_name = ''
    print(class_name)
    return render_template('score_manage.html', user_role=user_role, rep=rep, class_name=class_name, my_class=my_class,
                           semester=semester)


def add_score(student_id):
    score_info = request.json
    score = score_info['score']
    type_score = score_info['type_score']
    class_name = score_info['class_name']
    semester = score_info['semester']
    subject_name = score_info['subject_name']
    year = score_info['year']
    msg_ex = None

    try:
        check = dao.check_student_class_semester(student_id=int(student_id), class_name=class_name, year=year)
        score = float(score)
        if 0 <= score <= 10:
            print(msg_ex)
            if check:
                dao.save_score(student_id, score, type_score, class_name, semester, subject_name, year)
                msg_ex = 204
                print(msg_ex)
            else:
                msg_ex = 502
        else:
            raise Exception(501)

    except Exception as ex:
        if ex.__eq__(501):
            return jsonify({'status': 501})
        else:
            return jsonify({'status': 500})
    else:
        return jsonify({
            'status': msg_ex,
            'score': {
                'score': score,
                'type_score': type_score,
                'class_name': class_name,
                'semester': semester,
                'subject_name': subject_name,
                'year': year,
                'student_id': student_id
            }
        })


def score_detail(student_id):
    subject = dao.subject()
    user_role = check_user_role()
    std = dao.get_student_by_id(student_id=student_id)
    return render_template('score_detail.html', student=std, user_role=user_role, subject=subject)


def del_score(student_id):
    score = request.json
    score_id = 0
    data = []
    score_id = score['score_id']
    test = dao.delete_score(int(score_id))
    if test:
        data.append({
            'status': 204,
            "score_id": score_id
        })
    else:
        data.append({
            'status': 500,

        })

    print(data)
    return jsonify(data)


def update_score(student_id):
    score = request.json
    score_id = 0
    data = []
    print(score)
    score_id = score['score_id']
    score_value = score['score_value']

    test = dao.update_score(int(score_id), score_value)
    score_value = float(score_value)
    if 0 <= score_value <= 10:
        if test:
            data.append({
                'status': 204,
                "score_id": score_id,
                "score_value": score_value
            })
    else:
        data.append({
            'status': 500
        })
    print(data)
    return jsonify(data)


def load_score_detail(student_id):
    rep = dao.get_student_by_id(student_id=student_id)
    data = []

    print("rep")
    print(rep)
    print("rep")
    print(rep.score)
    for s in rep.score:
        print(s)
        print(s.id)
        data.append({
            'score_id': s.id,
            'score': s.score,
            'type_score': s.type_score,
            'subject_name': s.subject.name,
            'semester': s.semester.semester,
            'year': s.semester.year,
            'student_id': s.student.id
        })
    return jsonify(data)


def score_average():
    user_role = check_user_role()
    class_name = request.args.get('class-name')
    year = request.args.get('year')
    if year:
        subject = dao.subject()
        rep = dao.score_average(year)
        data = utils.check_list(rep, class_name)
        score = utils.cal_avg(data, subject)
    else:
        score = None
    return render_template('average.html', score=score, year=year, user_role=user_role)


def inform():
    rep = dao.teach_class(kw=request.args.get('keyword'))
    user_role = check_user_role()
    return render_template('inform_user.html', user_role=user_role, rep=rep)


def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
        return redirect('/admin')
    else:
        return redirect('/')


def logout_my_user():
    logout_user()
    return redirect('/')


@anonymous_user
def login_my_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        try:
            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user=user)
            else:
                err_msg = "Đăng nhập thất bại"
        except Exception as ex:
            err_msg = ex

    user = current_user
    return index()


def student():
    user_role = check_user_role()
    key = app.config['STUDENT']
    student_session = session.get(key, {})
    name = dao.student()
    kw = request.args.get("keyword")
    if not kw:
        kw = ''
    for i in name:
        if str(kw) in i.name or kw == str(i.id):
            if i.id not in student_session:
                student_session[i.id] = {
                    "student_id": i.id,
                    "student_name": i.name,
                    "student_sex": i.sex,
                    "student_address": i.address,
                    "student_dob": i.dob,
                    "student_mail": i.email,
                }
    return render_template('student.html', user_role=user_role)


def load_student():
    pass


def add_student():
    student_info = request.json
    student_name = student_info['student_name']
    student_sex = student_info['student_sex']
    student_dob = student_info['student_dob']
    student_address = student_info['student_address']
    student_email = student_info['student_email']
    key = app.config['STUDENT']
    student_session = session.get(key, {})
    try:
        if not student_name:
            return jsonify({
                'error': "Chưa nhập tên"
            })
        if not student_dob:
            return jsonify({
                'error': "Chưa chọn ngày sinh"
            })
        if not student_address:
            return jsonify({
                'error': "Chưa nhập địa chỉ"
            })
        if not dao.check_age(student_dob):
            return jsonify({
                'error': "Tuổi không hợp lệ"
            })
    except:
        return jsonify({
            'error': "Lỗi"
        })
    else:
        name = dao.add_student(student_name=student_name, student_sex=student_sex, student_dob=student_dob,
                               student_address=student_address, student_email=student_email)
        if len(name) not in student_session:
            student_session[len(name)] = {
                "student_id": print(len(name)),
                "student_name": student_name,
                "student_sex": student_sex,
                "student_address": student_address,
                "student_dob": student_dob,
                "student_mail": student_email,
            }
        return jsonify({
            'error': "Thêm thành công"
        })


def update_student():
    student_info = request.json
    student_id = student_info['student_id']
    student_name = student_info['student_name']
    student_sex = student_info['student_sex']
    student_dob = student_info['student_dob']
    student_address = student_info['student_address']
    student_email = student_info['student_email']
    key = app.config['STUDENT']
    student_session = session.get(key, {})
    print(student_session)
    try:
        if not student_name:
            return jsonify({
                'error': "Chưa nhập tên"
            })
        if not student_dob:
            return jsonify({
                'error': "Chưa chọn ngày sinh"
            })
        if not student_address:
            return jsonify({
                'error': "Chưa nhập địa chỉ"
            })
        if not dao.check_age(student_dob):
            return jsonify({
                'error': "Tuổi không hợp lệ"
            })
    except:
        return jsonify({
            'error': "Lỗi server"
        })
    else:
        check = dao.update_student(student_id=student_id, student_name=student_name, student_address=student_address, student_dob=student_dob, student_mail=student_email)
        if int(student_id) == student_session:
            student_session['student_name'] = student_name
            student_session['student_address'] = student_address
            student_session['student_dob'] = student_dob
            student_session['student_mail'] = student_email
        session[key] = student_session
        if check:
            return jsonify({
                        'error': "Cập nhật thành công"
                    })
        else:
            return jsonify({
                'error': "Cập nhật không thành công"
            })
