from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms import TextAreaField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email

class CreateCourseForm(FlaskForm):
    course_name = StringField('课程名', validators=[DataRequired()])
    submit = SubmitField('提交')