from Stud_Man import app, admin, login, controller, utils
from flask import session
import dao


app.add_url_rule('/', 'index', controller.index)
app.add_url_rule('/admin-login', 'admin-login', controller.admin_login, methods=['post'])
app.add_url_rule('/logout', 'logout', controller.logout_my_user)
app.add_url_rule('/', 'login-user', controller.login_my_user, methods=['get', 'post'])
app.add_url_rule('/search', 'search_student', controller.search_student)
app.add_url_rule('/inform', 'user-inform', controller.inform)
app.add_url_rule('/score', 'score', controller.score_manage)
app.add_url_rule('/score/average', 'score-average', controller.score_average)
app.add_url_rule('/score/<student_id>', 'score-detail', controller.score_detail)
app.add_url_rule('/api/score/<student_id>/score-list', 'add-score', controller.add_score, methods=['post'])
app.add_url_rule('/api/score/<student_id>/score-list', 'update-score', controller.update_score, methods=['update'])
app.add_url_rule('/api/score/<student_id>/score-list', 'delete-cart', controller.del_score, methods=['delete'])
app.add_url_rule('/api/score/<student_id>/score-list', 'score-detail-load', controller.load_score_detail)
app.add_url_rule('/student', 'student', controller.student)
app.add_url_rule('/api/student/add-student', 'add-student', controller.add_student, methods=['post'])
app.add_url_rule('/api/student/add-student', 'update-student', controller.update_student, methods=['update'])
app.add_url_rule('/build-class', 'class-list', controller.build_class)
app.add_url_rule('/api/build-class/<class_id>/list', 'add-to-list', controller.add_student_list)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
