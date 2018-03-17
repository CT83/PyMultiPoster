from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class TumblrPostForm(FlaskForm):
    blog_name = StringField('Blog Name', validators=[InputRequired(),
                                                     Length(min=1, max=100)])

    title = StringField('Title', validators=[Length(min=1, max=150)])
    post = TextAreaField('Post', render_kw={"rows": 10, "cols": 70},
                         validators=[InputRequired(), Length(min=10, max=470000)])
    image = StringField('Image')

    submit = SubmitField('Post and Proceed')
