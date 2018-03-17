from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class FacebookPostForm(FlaskForm):
    page_id = StringField('Page Id (Optional, Keep empty if you want to post to your own Wall)',
                          validators=[Length(max=17)])
    title = StringField('Title', validators=[Length(max=100)])
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=4, max=63000)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
