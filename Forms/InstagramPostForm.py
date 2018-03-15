from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


# TODO Create proper formatted forms for all the social networks used

class InstagramPostForm(FlaskForm):
    post = TextAreaField('Post', render_kw={"rows": 5, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Confirm Manual Post & Proceed')
