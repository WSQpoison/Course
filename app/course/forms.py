from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms import TextAreaField, DateTimeField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email

class CreateCourseForm(FlaskForm):
    course_name = StringField('课程名', validators=[DataRequired()])
    submit = SubmitField('提交')

class PublishHomeworkForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    description = PageDownField('题目描述')
    begin_time = DateTimeField('开始时间', validators=[DataRequired()])
    end_time = DateTimeField('结束时间', validators=[DataRequired()])
    submit = SubmitField('发布')
