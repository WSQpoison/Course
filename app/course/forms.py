from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from flask_wtf.file import FileRequired
from wtforms import TextAreaField, DateTimeField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email

class CreateCourseForm(FlaskForm):
    course_name = StringField('课程名', validators=[DataRequired()])
    student_list = FileField('学生名单')
    submit = SubmitField('提交')
