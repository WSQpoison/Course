import os
import random
import csv

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

    return render_template('courses/course_list.html', courses=courses)

@course.route('/create-course', methods=['GET', 'POST'])
@login_required
def course_create():
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(name=form.course_name.data)
        role = Role(role='teacher')
        role.user = current_user
        role.course = course

        file = form.student_list.data
        if file != '':
            rand_filename = str(random.randint(0, 100000)) \
                            + secure_filename(file.filename)
            path = 'app/static/tmp'
            os.makedirs(path, exist_ok=True)
            file.save(os.path.join(path, rand_filename))
            add_member(os.path.join(path, rand_filename), course)
            os.remove(os.path.join(path, rand_filename))
            
        db.session.add(course)
        db.session.add(role)
        db.session.commit()
        flash('课程创建成功')
        return redirect(url_for('.course_list'))
    return render_template('courses/course_create.html', form=form) 

@course.route('/course/<id>')
def course_page(id):
    course = Course.query.get_or_404(id)
    return render_template('courses/course.html', course=course, teacher=getTeacher(course))

def createUser(id, name):
    u = User(id=id, name=name, password=str(id))
    db.session.add(u)
    return u

def add_member(filename, course):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = User.query.get(row['id'])
            if not user:
                user = createUser(row['id'], row['name'])
            role = Role(role='student')
            role.user = user
            role.course = course
            db.session.add(role)
            