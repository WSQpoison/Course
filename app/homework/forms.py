from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from flask_wtf.file import FileRequired
from wtforms import TextAreaField, DateTimeField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email

class PublishHomeworkForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    description = PageDownField('题目描述')
    begin_time = DateTimeField('开始时间', validators=[DataRequired()])
    end_time = DateTimeField('结束时间', validators=[DataRequired()])
    file = FileField('文件')
    submit = SubmitField('发布')

class SubmitHomeworkForm(FlaskForm):
    file = FileField('提交', validators=[FileRequired('文件未选择')])
    submit = SubmitField('提交作业')