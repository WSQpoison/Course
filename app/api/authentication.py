from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g
from . import api
from ..models import *
from .error import *

auth = HTTPBasicAuth()

@api.route('/token')
@auth.login_required
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')

    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600),
                    'expiration': 3600})

@auth.verify_password
def verify_password(id_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(id_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(id=id_or_token).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credendtials')