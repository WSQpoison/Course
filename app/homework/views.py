import os
import random
import zipfile

from . import homework
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request, send_from_directory, send_file
from flask_login import UserMixin, login_required
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from .forms import *
from ..models import *
from .. import db
from ..util import *

@homework.route('/course/<int:id>/homework-list')
def homework_list(id):
    course = Course.query.get_or_404(id)
    return render_template('homeworks/homework_list.html', course=course)

@homework.route('/course/<int:id>/homework/<int:hw_id>')
@login_required
def homework_page(id, hw_id):
    course = Course.query.get_or_404(id)
    homework = Homework.query.get_or_404(hw_id)
    if current_user.id in course.get_teacher():
        role = 'teacher'
    else:
        role = 'student'
    return render_template('homeworks/homework_page.html', course=course, hw=homework, role=role)

@homework.route('/course/<int:id>/homework-publish', methods=['GET', 'POST'])
@login_required
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
    return render_template('homeworks/homework_publish.html', form=form, course=course)

@homework.route('/course/<int:id>/homework/<int:hw_id>/get')
@login_required
def homework_get(id, hw_id):
    path = 'app/static/course/%d/%d' % (id, hw_id)
    filelists = os.listdir(path)
    if len(filelists) < 1:
        flash('No homework info file')
        return redirect(url_for('.homework_page', id=id, hw_id=hw_id))
    else:
        print(path)
        filename = filelists[0]
    return send_from_directory(directory=path[4:], filename=filename, as_attachment=True)

@homework.route('/course/<int:id>/homework/<int:hw_id>/download', methods=['GET', 'POST'])
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
    return redirect(url_for('.homework_page', id=id, hw_id=hw_id))

@homework.route('/course/<int:id>/homework/<int:hw_id>/submit', methods=['GET', 'POST'])
@login_required
def homework_submit(id, hw_id):
    """Student submits homework.
    """
    course = Course.query.get_or_404(id)
    form = SubmitHomeworkForm()
    if form.validate_on_submit():
        file = form.file.data
        path = 'app/static/course/%d/%d' % (id, hw_id)
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        print(path)
        print(filename)
        flash('Successful submit!')
        return redirect(url_for('.homework_page', id=id, hw_id=hw_id))
    return render_template('homeworks/homework_submit.html', form=form, course=course, id=id, hw_id=hw_id)
