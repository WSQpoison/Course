import os

from .models import *

def getTeacher(course):
    for role in course.users:
        if role.role == 'teacher':
            return role.user

def get_user_head(id):
    head = '/static/heads/default.jpg'
    f = [f for f in os.listdir('app/static/heads') \
               if f.startswith(str(id))]
    if len(f) != 0:
        head = os.path.join('/static/heads', f[0])
    return head