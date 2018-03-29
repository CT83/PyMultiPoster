from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import InputRequired, Length


class InstagramPostForm(FlaskForm):
    post = TextAreaField('Post', render_kw={"rows": 5, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    image = StringField('Image')
    submit = SubmitField('Queue & Proceed')
