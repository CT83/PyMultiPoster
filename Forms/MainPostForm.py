from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, TextAreaField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import InputRequired, Length

from Forms.custom_validators.ImageFileRequired import ImageFileRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MainPostForm(FlaskForm):
    title = StringField('Title (Optional)', validators=[Length(max=100)])
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    photo = FileField('Photo (Optional)', validators=[ImageFileRequired()])

    selected_socialnetworks = MultiCheckboxField('Social Networks', validators=[InputRequired()])
    submit = SubmitField('Proceed')
