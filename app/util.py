from .models import *

def getTeacher(course):
    for role in course.users:
        if role.role == 'teacher':
            return role.user