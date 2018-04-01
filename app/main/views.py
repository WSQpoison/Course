import os
import random

from . import main
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_login import UserMixin, login_required
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from .forms import *
from ..models import *
from .. import db
from ..util import *

basedir = 'app'

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.user_profile', id=current_user.id))
    return redirect('/login')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, False)
            return redirect(request.args.get('next')
                            or url_for('.post'))
        flash('学号或密码错误')
    return render_template('login.html', form=form)

@main.route('/users')
def users():
    flash('请先登录')
    return redirect('/login')

@main.route('/user_profile/<id>')
def user_profile(id):
    head = get_user_head(id)
    user = User.query.filter_by(id=id).first()
    return render_template('user_profile.html', user=user, head=head)

@main.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    head = get_user_head(current_user.id)
    return render_template('posts.html', form=form, posts=posts, head=head)

@main.route('/asjdfoijqwe')
def get_form():
    return json

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        head = form.head.data
        if head != '':
            for f in os.listdir('app/static/heads'):
                if f.startswith(str(current_user.id)):
                    os.remove(os.path.join('app/static/heads', f))
            filename = secure_filename(head.filename)
            head.save(os.path.join(
                basedir, 'static', 'heads',
                str(current_user.id) + str(random.choice(range(100))) + '.jpg'
            ))
        db.session.add(current_user)
        db.session.commit()
        flash('个人简介更新成功')
        return redirect(url_for('.user_profile', id=current_user.id))
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@main.route('/create-course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(name=form.course_name.data)
        role = Role(role='teacher')
        role.user = current_user
        role.course = course
        db.session.add(course)
        db.session.add(role)
        db.session.commit()
        flash('课程创建成功')
        return redirect(url_for('.course_list'))
    return render_template('create_course.html', form=form)

@main.route('/course-list')
@login_required
def course_list():
    courses = []
    for role in current_user.courses:
        for user in role.course.users:
            if user.role == 'teacher':
                teacher = user.user
        courses.append((role.course, teacher))

    return render_template('course_list.html', courses=courses)

def get_user_head(id):
    head = '/static/heads/default.jpg'
    f = [f for f in os.listdir('app/static/heads') \
               if f.startswith(str(id))]
    if len(f) != 0:
        head = os.path.join('/static/heads', f[0])
    return head
