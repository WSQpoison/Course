import os
import random
import csv
import zipfile

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
    if current_user.id in course.get_teacher():
        role = 'teacher'
    else:
        role = 'student'
    return render_template('homework.html', course=course, hw=homework, role=role)

@course.route('/course/<int:id>/homework/<int:hw_id>/get')
def homework_get(id, hw_id):
    path = 'app/static/course/%d/%d' % (id, hw_id)
    filelists = os.listdir(path)
    if len(filelists) < 1:
        flash('No homework info file')
        return redirect(url_for('.homework', id=id, hw_id=hw_id))
    else:
        print(path)
        print(filename)
        filename = filelists[0]
    return send_from_directory(directory=path[4:], filename=filename, as_attachment=True)

@course.route('/course/<int:id>/homework-publish', methods=['GET', 'POST'])
def homework_publish(id):
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

        path = 'app/static/course/%d/%d' % (id, hw.id)
        os.makedirs(path, exist_ok=True)
        if file != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))

        return redirect(url_for('.homework_list', id=id))
    return render_template('publish_homework.html', form=form, course=course)

@course.route('/course/<int:id>/homework/<int:hw_id>/download', methods=['GET', 'POST'])
@login_required
def homework_download(id, hw_id):
    """Teacher downloads the students' homeworks.
    This comment will be completed next time.
    """
    path = 'app/static/course/%d/%d' % (id, hw_id)
    if os.path.exists(path):
        course = Course.query.get_or_404(id)
        homework = Homework.query.get_or_404(hw_id)
        filelists = os.listdir(path)
        print(filelists)

        if filelists == None or len(filelists) < 1:
            print('No homework submitted!')
        else:
            zipname = course.name + '_' + homework.title + '.zip'
            zippath = path + '/' + zipname
            if os.path.exists(zippath):
                os.remove(zippath)
                filelists.remove(zipname)
                print(filelists)
            zip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in filelists:
                filepath = os.path.join(path, file)
                zip.write(filepath, file)
            zip.close()
            return send_from_directory(directory=path[4:], filename=zipname, as_attachment=True)
    return redirect(url_for('.homework', id=id, hw_id=hw_id))

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
            