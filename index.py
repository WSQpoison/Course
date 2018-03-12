import os
import random

from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

sid_length = 8

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def verify_password(self, pw):
        return pw == self.password

class LoginForm(FlaskForm):
    id = StringField('账号', validators=[DataRequired(), Length(min=sid_length, \
                                                                max=sid_length)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class EditForm(FlaskForm):
    head = FileField('选择图片')
    email = StringField('邮箱', validators=[Email()])
    submit = SubmitField('提交')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user_profile', id=current_user.id))
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, False)
            return redirect(request.args.get('next')
                            or url_for('user_profile', id=user.id))
        flash('学号或密码错误')
    return render_template('login.html', form=form)

@app.route('/users')
def users():
    flash('请先登录')
    return redirect('/login')

@app.route('/user_profile/<id>')
def user_profile(id):
    if not current_user.is_authenticated or current_user.id != int(id):
        flash('请先登录')
        return redirect('/login')
    head = '/static/heads/default.jpg'
    f = [f for f in os.listdir('static/heads') \
               if f.startswith(str(current_user.id))]
    if len(f) != 0:
        head = os.path.join('/static/heads', f[0])
    return render_template('user_profile.html', user=current_user, head=head)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        head = form.head.data
        if head != '':
            for f in os.listdir('static/heads'):
                if f.startswith(str(current_user.id)):
                    os.remove(os.path.join('static/heads', f))
            filename = secure_filename(head.filename)
            head.save(os.path.join(
                basedir, 'static', 'heads',
                str(current_user.id) + str(random.choice(range(100))) + '.jpg'
            ))
        db.session.add(current_user)
        db.session.commit()
        flash('个人简介更新成功')
        return redirect(url_for('user_profile', id=current_user.id))
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def validate(sid, password):
    std_password = get_password(sid)
    if std_password == password:
        return True
    else:
        return False

def get_password(sid):
    return users.get(sid, None)

if __name__ == '__main__':
    manager.run()
