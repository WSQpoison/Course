import os
import random

from . import course
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_login import UserMixin, login_required
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from .forms import *
from ..models import *
from .. import db
from ..util import *

@course.route('/course-list')
@login_required
def course_list():
    courses = []
    for role in current_user.courses:
        for user in role.course.users:
            if user.role == 'teacher':
                teacher = user.user
        courses.append((role.course, teacher))

    return render_template('course_list.html', courses=courses)

@course.route('/create-course', methods=['GET', 'POST'])
@login_required
def course_create():
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
    return render_template('course_create.html', form=form) 

@course.route('/course/<id>')
def course_page(id):
    course = Course.query.get_or_404(id)
    return render_template('course.html', course=course, teacher=getTeacher(course))

@course.route('/course/<id>/homework-list')
def homework_list(id):
    return '<h1> not yet implement </h1>'

@course.route('/course/<id>/publish-homework')
def publish_homework(id):
    course = Course.query.get_or_404(id)
    return '<h1> not yet implement </h1>'