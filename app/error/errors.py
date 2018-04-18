from flask import render_template
from . import error

@error.app_errorhandler(401)
def unauthorized_handler(e):
    return render_template('errors/error_401.html'), 401

@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/error_404.html'), 404

@error.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/error_500.html'), 500
