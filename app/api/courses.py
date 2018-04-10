from flask import jsonify

from . import api
from .authentication import auth
from ..models import *

@api.route('/course/<id>')
# @auth.login_required
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_json())

@api.route('/courses/')
@auth.login_required
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_json() for course in courses])
