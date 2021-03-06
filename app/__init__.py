from flask import Flask, render_template
# from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
loginManager = LoginManager()
moment = Moment()
pagedown = PageDown()

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    loginManager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    from .profile import profile as profile_blueprint
    from .course import course as course_blueprint
    from .homework import homework as homework_blueprint
    from .error import error as error_buleprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(homework_blueprint)
    app.register_blueprint(error_buleprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
