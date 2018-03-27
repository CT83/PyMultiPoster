from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class LinkedInPostForm(FlaskForm):
    page_id = StringField('Company Page ID (Optional, '
                          'Keep empty if you want to post to your own Page)',
                          validators=[Length(max=17)])
    title = StringField('Title', validators=[Length(min=4, max=100)])

    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=119000)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
