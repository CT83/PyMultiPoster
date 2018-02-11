from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired


class InstagramLoginForm(FlaskForm):
    email = EmailField('Email:', [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')
