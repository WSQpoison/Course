import os
import random

from . import main
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

from .forms import LoginForm, EditForm
from ..models import User
from .. import db

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
                            or url_for('.user_profile', id=user.id))
        flash('学号或密码错误')
    return render_template('login.html', form=form)

@main.route('/users')
def users():
    flash('请先登录')
    return redirect('/login')

@main.route('/user_profile/<id>')
def user_profile(id):
    if not current_user.is_authenticated or current_user.id != int(id):
        flash('请先登录')
        return redirect('/login')
    head = '/static/heads/default.jpg'
    f = [f for f in os.listdir('app/static/heads') \
               if f.startswith(str(current_user.id))]
    if len(f) != 0:
        head = os.path.join('/static/heads', f[0])
    return render_template('user_profile.html', user=current_user, head=head)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        head = form.head.data
        print('%r' % head)
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
def logout():
    logout_user()
    return redirect(url_for('.index'))

if __name__ == '__main__':
    manager.run()
