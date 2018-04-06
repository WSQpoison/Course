from . import api
from ..models import *

@api.route('/course/<id>')
# @auth.login_required
def get_course(id):
    course = Course.query.get_or_404(id)
    return course.to_json()
