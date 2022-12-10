import flask_login
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.functions import current_user

from Stud_Man import app, admin, login, controller, utils
from flask import render_template, redirect, request, session, jsonify
import dao
from Stud_Man.models import UserRole, Semester, Subject, MyClass, Student
from Stud_Man.decorators import anonymous_user
from Stud_Man.utils import *


@app.route("/")
def index():
    user_role = check_user_role()
    rep = dao.teach_class(kw=request.args.get('keyword'))
    return render_template('index.html', rep=rep, user_role=user_role)


@app.route("/search")
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


@app.route('/score')
def score_manage():
    user_role = check_user_role()
    semester = dao.semester()
    subject = dao.subject()
    student = dao.student()
    my_class = dao.my_class()

    return render_template('score_manage.html', user_role=user_role, student=student,
                           subject=subject, semester=semester, my_class=my_class)


@app.route('/api/score/score-list')
def load_score():
    rep = dao.student_score()
    kw = request.args.get('keyword')
    data = []
    if kw:
        kw = kw
    else:
        kw = ''

    for s in rep:
        if kw in s.student.name:
            data.append({
                'score_id': s.id,
                'student_name': s.student.name,
                'score': s.score,
                'type_score': s.type_score,
                'class_name': s.my_class.name,
                'semester': s.semester.semester,
                'subject_name': s.subject.name,
                'year': s.semester.semester
            })
    return jsonify(data)


@app.route('/api/score/score-list', methods=['post'])
def add_score():
    score_info = request.json
    student_name = score_info['student_name']
    score = score_info['score']
    type_score = score_info['type_score']
    class_name = score_info['class_name']
    semester = score_info['semester']
    subject_name = score_info['subject_name']
    year = score_info['year']
    msg_ex = None

    try:
        check = dao.check_student_class_semester(student_name=student_name, class_name=class_name, semester=semester, year=year)
        print(check)
        print(score)
        if 0 <= int(score) <= 10:
            print(msg_ex)
            if check:
                dao.save_score(student_name, score, type_score, class_name, semester, subject_name, year)
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
                'student_name': student_name,
                'score': score,
                'type_score': type_score,
                'class_name': class_name,
                'semester': semester,
                'subject_name': subject_name,
                'year': year
            }
        })


@app.route("/inform")
def inform():
    rep = dao.teach_class(kw=request.args.get('keyword'))
    user_role = check_user_role()
    return render_template('inform_user.html', user_role=user_role, rep=rep)


@app.route('/admin-login', methods=['post'])
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


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route('/', methods=['get', 'post'])
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


if __name__ == '__main__':
    app.run(debug=True)
