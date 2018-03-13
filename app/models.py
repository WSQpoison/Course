from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db, loginManager

class User(UserMixin, db.Model):
    '''
    用户数据模型
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def verify_password(self, pw):
        return pw == self.password

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
