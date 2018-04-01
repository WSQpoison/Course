from . import api
from ..models import *

@api.route('/user/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return user.to_json()
