import os

from app import create_app, db
from app.models import User
from flask_script import Manager, Shell

app = create_app('development')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command('shell', Shell(make_context=make_shell_context))

def quick_db():
    '''
    用于开发阶段快速生成数据库
    '''
    db.create_all()
    u1 = User(id='11111111', name='狗蛋', password='abc', email='111@qq.com')
    u2 = User(id='22222222', name='二狗', password='abc', email='222@qq.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
