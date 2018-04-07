import os
import random

from . import course
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request, send_from_directory, send_file
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

@course.route('/course/<int:id>/homework-list')
def homework_list(id):
    course = Course.query.get_or_404(id)
    return render_template('homework_list.html', course=course)

@course.route('/course/<int:id>/homework/<int:hw_id>')
def homework(id, hw_id):
    course = Course.query.get_or_404(id)
    homework = Homework.query.get_or_404(hw_id)

    return render_template('homework.html', course=course, hw=homework)

@course.route('/course/<int:id>/homework/<int:hw_id>/download/')
def homework_download(id, hw_id):
    path = 'app/static/course/%d/%d' % (id, hw_id)
    filename = os.listdir(path)[0]
    print(path)
    print(filename)

    return send_from_directory(directory=path[4:], filename=filename, as_attachment=True)

@course.route('/course/<int:id>/publish-homework', methods=['GET', 'POST'])
def publish_homework(id):
    form = PublishHomeworkForm()
    course = Course.query.get_or_404(id)

    if form.validate_on_submit():
        title = form.title.data
        desc = form.description.data
        begin = form.begin_time.data
        end = form.end_time.data
        file = form.file.data

        hw = Homework(title=title, description=desc, begin_time=begin,
                      end_time=end, course=course)
        db.session.add(hw)
        db.session.commit()
        if file != '':
            path = 'app/static/course/%d/%d' % (id, hw.id)
            os.makedirs(path, exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))

        return redirect(url_for('.homework_list', id=id))
    return render_template('publish_homework.html', form=form, course=course)
