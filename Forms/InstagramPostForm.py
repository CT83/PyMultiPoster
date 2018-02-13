from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


# TODO Create proper formatted forms for all the social networks used

class InstagramPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=1, max=100)])

    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=80)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
