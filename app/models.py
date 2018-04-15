from flask import jsonify, current_app
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from . import db, loginManager

class User(UserMixin, db.Model):
    '''
    用户数据模型
    '''
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(64), nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    courses = db.relationship('Role', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def verify_password(self, pw):
        return pw == self.password

    def to_json(self):
        json_user = {
            user_id: self.id,
            user_name: self.name,
            registerTime: self.registerTime,
            email: self.email,
            courses: self.get_courses()
        }
        return json_user

    def get_courses(self):
        return [course.course_id for course in self.courses]

class Role(db.Model):
    __tablename__ = 'roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
                          primary_key=True)
    role = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='courses')
    course = db.relationship('Course', back_populates='users')

class Course(db.Model):
    '''
    课程数据模型
    '''
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    users = db.relationship('Role', back_populates='course')
    homework = db.relationship('Homework', backref='course', lazy='dynamic')

    def to_json(self):
        users = self.get_users()
        students = self.get_students()
        teacher = self.get_teacher()
        json_course = {
            'course_id': self.id,
            'course_name': self.name,
            'students': students,
            'teacher': teacher,
        }
        return json_course

    def get_users(self):
        return [{'user_id':role.user_id, 'role':role.role} 
                for role in self.users]

    def get_students(self):
        users = self.get_users()
        return [user['user_id'] for user in users if user['role'] == 'student']

    def get_teacher(self):
        users = self.get_users()
        return [user['user_id'] for user in users if user['role'] == 'teacher']

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return 'Post %d' % self.id

class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    begin_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    @staticmethod
    def on_changed_description(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.description_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    
    def __repr__(self):
        return '<Homework %s %d>' % (self.title, self.id)


db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Homework.description, 'set', Homework.on_changed_description)

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
