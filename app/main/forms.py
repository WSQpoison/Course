from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email

sid_length = 8

class LoginForm(FlaskForm):
    '''
    登录界面使用的表单
    '''
    id = StringField('账号', validators=[DataRequired(), Length(min=sid_length, \
                                                                max=sid_length)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class EditForm(FlaskForm):
    '''
    编辑个人资料界面使用的表单
    '''
    head = FileField('选择图片')
    email = StringField('邮箱', validators=[Email()])
    submit = SubmitField('提交')
