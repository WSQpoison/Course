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
        return redirect(url_for('profile.user_profile', id=current_user.id))
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

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))