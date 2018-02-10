from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class MainPostForm(FlaskForm):
    title = StringField('title', validators=[Length(min=6, max=20)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=80)])
    photo = FileField('Your photo')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
