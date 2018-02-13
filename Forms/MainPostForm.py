from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, TextAreaField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import InputRequired, Length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MainPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=6, max=20)])
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    photo = FileField('Photo (Optional)')

    string_of_files = ['Facebook\r\nInstagram\r\nTumblr\r\nLinkedIn\r\nTwitter\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    selected_socialnetworks = MultiCheckboxField('Social Networks', choices=files)
    submit = SubmitField('Proceed')
