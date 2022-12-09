from Stud_Man import db, app, dao
from Stud_Man.models import Regulation, User, UserRole, Subject
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class RegulationView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    # column_filters = ('id', 'user.name')
    column_labels = {
        'user': 'Người chỉnh sửa'
    }
    page_size = 6
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


class SubjectView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    # column_filters = ('content', 'id', 'user.name')
    column_labels = {
        'score': 'Nội dung',
        'user': 'Người chỉnh sửa'
    }
    page_size = 6
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }



admin = Admin(app=app, name="Quan ly hoc sinh", template_mode="bootstrap4")
admin.add_view(RegulationView(Regulation, db.session, name='Quy định'))
admin.add_view(SubjectView(Subject, db.session, name='Môn học'))
admin.add_view(LogoutView(name='Đăng xuất'))