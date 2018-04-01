import os
import random

from . import management
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_login import UserMixin, login_required
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import secure_filename

# from .forms import *
from ..models import *
from .. import db
from ..util import *

@management.route('/course/<id>')
def course(id):
    course = Course.query.get_or_404(id)
    return render_template('course.html', course=course, teacher=getTeacher(course))

@management.route('/course/<id>/homework-list')
def homework_list(id):
    return '<h1> not yet implement </h1>'

@management.route('/course/<id>/publish-homework')
def publish_homework(id):
    course = Course.query.get_or_404(id)
    return '<h1> not yet implement </h1>'
        