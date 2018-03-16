from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class InstagramPostForm(FlaskForm):
    post = TextAreaField('Post', render_kw={"rows": 5, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Confirm Manually Posted & Proceed')
