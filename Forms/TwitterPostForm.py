from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class TwitterPostForm(FlaskForm):
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=10, max=140)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
