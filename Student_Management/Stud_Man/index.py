import flask_login
from flask_login import login_user, login_required, logout_user, current_user
from Stud_Man import app, admin, login, controller, utils
from flask import render_template, redirect, request, session, jsonify
import dao
from Stud_Man.models import UserRole
from Stud_Man.decorators import anonymous_user
from Stud_Man.utils import *


@app.route("/")
def index():
    user_role = check_user_role()
    rep = dao.teach_class(kw=request.args.get('keyword'))
    return render_template('index.html', rep=rep, user_role=user_role)


@app.route("/search")
def search_student():
    rep = dao.teach_class(kw=request.args.get('keyword'))
    user_role = check_user_role()
    name = dao.student_search(student_name=request.args.get('student-name'),
                              student_class=request.args.get('student-class'),
                              student_mshs=request.args.get('student-mshs'))
    return render_template('search_student.html', name=name, user_role=user_role, rep=rep)


@app.route('/score')
def score_manage():
    rep = dao.student_score(kw=request.args.get('keyword'))
    add = dao.student_score('')
    student_name = dao.select_student()
    class_name = dao.select_class()
    semester = dao.select_semester()
    user_role = check_user_role()
    # score_15p = []
    # score_45p = []
    # score_ck = []

    # for s in rep:
    #     student_name = s[0]
    #     score_value = s[1]
    #     score_id = str(s[2])
    #     type_score = s[3]
    #     class_name = s[4]
    #     key = app.config['SCORE_KEY']
    #     score = session.get(key, {})
    #     if score_id not in score:
    #         score[score_id] = {
    #             "stud_name": student_name,
    #             "type_sco": type_score,
    #             "score_id": score_id,
    #             "score_val": score_value,
    #             "cl_name": class_name
    #         }
    # session[key] = score

    return render_template('score_manage.html', user_role=user_role, rep=rep, add=add, student_name=student_name,
                           class_name=class_name, semester=semester)


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
