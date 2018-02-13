from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length


class InstagramLoginForm(FlaskForm):
    username = StringField('Instagram Username', validators=[DataRequired(),
                                                             Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')
