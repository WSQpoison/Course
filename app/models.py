from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from markdown import markdown
import bleach
from . import db, loginManager

class User(UserMixin, db.Model):
    '''
    用户数据模型
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(64), nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    def verify_password(self, pw):
        return pw == self.password

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
        return 'Post %d' % id

db.event.listen(Post.body, 'set', Post.on_changed_body)

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
