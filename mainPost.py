from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename, redirect

from Forms.FacebookPostForm import FacebookPostForm
from Forms.MainPostForm import MainPostForm
from Forms.TwitterPostForm import TwitterPostForm
from SessionManagement import clear_session, save_session, retrieve_session

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "powerful secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "powerful secretkey"
bootstrap = Bootstrap(app)


@app.route('/main', methods=('GET', 'POST'))
def main():
    form = MainPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        social_networks = form.selected_socialnetworks.data
        try:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save("tmp/" + filename)
        except AttributeError:
            filename = None
        print("main() Submitted Form...")
        print("Title:", title)
        print("Post:", post)
        print("Social Networks:", social_networks)
        print("Image:", filename)
        save_session(filename, post, title)
        return redirect('/facebook_poster')
        # return render_template('post/main.html', form=form, filename=filename)
    return render_template('post/main.html', form=form, )


@app.route('/facebook_poster', methods=('GET', 'POST'))
def facebook_poster():
    print("Facebook Poster...")
    title, post, image = retrieve_session()
    form = FacebookPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        image = form.image.data

        print("Posting to Facebook...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        print("Redirecting to Twitter...")
        return redirect('/twitter_poster')
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/facebook_post.html', form=form, filename=image)


@app.route('/twitter_poster', methods=('GET', 'POST'))
def twitter_poster():
    print("Twitter Poster...")
    title, post, image = retrieve_session()
    form = TwitterPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        image = form.image.data

        print("Posting to Twitter...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/twitter_post.html', form=form, filename=image)


@app.route('/logout')
def logout():
    clear_session()


if __name__ == '__main__':
    app.run(debug=True)
