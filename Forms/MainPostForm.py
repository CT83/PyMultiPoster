from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, SubmitField, TextAreaField, SelectMultipleField
from wtforms import widgets, Form
from wtforms.validators import InputRequired, Length, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MainPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=6, max=20)])
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    photo = FileField('Photo (Optional)')

    string_of_files = ['FaceBook\r\nInstagram\r\nTumblr\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    selected_socialnetworks = MultiCheckboxField('Social Networks', choices=files)
    submit = SubmitField('Proceed')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
