from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms import TextAreaField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email

class EditForm(FlaskForm):
    '''
    编辑个人资料界面使用的表单
    '''
    head = FileField('选择图片')
    email = StringField('邮箱', validators=[Email()])
    submit = SubmitField('提交')