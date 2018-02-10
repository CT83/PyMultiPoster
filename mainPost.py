from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from Forms.MainPostForm import MainPostForm

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "powerful secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "powerful secretkey"
bootstrap = Bootstrap(app)


@app.route('/main', methods=('GET', 'POST'))
def upload():
    form = MainPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save("tmp/" + filename)

        print("Title:", title)
        print("Post:", post)
        print("Image:", filename)

    else:
        filename = None
    return render_template('post/main.html', form=form, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
