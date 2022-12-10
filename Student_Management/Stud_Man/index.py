import flask_login
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.functions import current_user

from Stud_Man import app, admin, login, controller, utils
from flask import render_template, redirect, request, session, jsonify
import dao
from Stud_Man.models import UserRole, Semester, Subject, MyClass, Student
from Stud_Man.decorators import anonymous_user
from Stud_Man.utils import *


app.add_url_rule('/', 'index', controller.index)
app.add_url_rule('/search', 'search_student', controller.search_student)
app.add_url_rule('/score', 'score', controller.score_manage)
app.add_url_rule('/api/score/score-list', 'score-list', controller.load_score)
app.add_url_rule('/api/score/score-list', 'add-score', controller.add_score, methods=['post'])
app.add_url_rule('/inform', 'user-inform', controller.inform)
app.add_url_rule('/admin-login', 'admin-login', controller.admin_login, methods=['post'])
app.add_url_rule('/logout', 'logout', controller.logout_my_user)
app.add_url_rule('/', 'login-user', controller.login_my_user, methods=['get', 'post'])


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
