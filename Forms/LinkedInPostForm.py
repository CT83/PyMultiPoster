from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class LinkedInPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=4, max=100)])

    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=119000)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
