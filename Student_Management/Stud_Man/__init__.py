from urllib.parse import quote
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = 'adfhkfh238ohfouaghfuoebf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/std-mana?charset=utf8mb4' % quote(
    '0979620120@Hau')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['STUDENT'] = 'student'
app.config['STUDENT-LIST'] = 'student_list'
db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)

@babel.localeselector
def load_locale():
    return 'vi'