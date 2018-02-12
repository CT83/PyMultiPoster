from flask import Flask, render_template, url_for, request, make_response
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename, redirect

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, \
    LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, TUMBLR_CLIENT_SECRET, TUMBLR_CLIENT_ID, LINKEDIN_RETURN_URL
from CookieManagement import set_cookie, get_cookie
from Forms.FacebookPostForm import FacebookPostForm
from Forms.InstagramLoginForm import InstagramLoginForm
from Forms.InstagramPostForm import InstagramPostForm
from Forms.LinkedInPostForm import LinkedInPostForm
from Forms.MainPostForm import MainPostForm
from Forms.TumblrPostForm import TumblrPostForm
from Forms.TwitterPostForm import TwitterPostForm
from SessionManagement import clear_session, save_session, retrieve_session, remove_session_socialnetwork, \
    store_list_session, retrieve_session_socialnetworks
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.LinkedIn.LinkedIn import LinkedIn, LinkedInAuth
from SocialMedia.Tumblr.Tumblr import Tumblr
from SocialMedia.Twitter.Twitter import Twitter

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
        save_session(filename, post, title, social_networks)
        print("Redirecting...")
        return redirect('/next_poster/main')
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

        facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                                 FACEBOOK_CLIENT_SECRET, 'AccessTokenSecret')
        if image not in 'None':
            print(facebook_user.publish_update(title + "\n" + post))
        else:
            # TODO Make this work
            print(facebook_user.publish_update_with_image_attachment(title + "\n" + post,
                                                                     image_url=image))

        print("Redirecting...")
        return redirect('/next_poster' + "/facebook")
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

        twitter_api = Twitter(TWITTER_CLIENT_ID,
                              TWITTER_CLIENT_SECRET,
                              "AccessToken", "AccessTokenSecret")

        if image not in 'None' and image not in "":
            print(twitter_api.publish_update(post))

        else:
            print(twitter_api.publish_update_with_image_attachment(post, image))

        print("Redirecting...")
        return redirect('/next_poster' + "/twitter")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/twitter_post.html', form=form, filename=image)


@app.route('/instagram_poster', methods=('GET', 'POST'))
def instagram_poster():
    print("Instagram Poster...")
    title, post, image = retrieve_session()
    form = InstagramPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        image = form.image.data

        print("Posting to Instagram...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)
        # TODO Add allow uploading if no image is selected
        # TODO Add upload to instagram logic here

        print("Redirecting...")
        return redirect('/next_poster' + "/instagram")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/instagram_post.html', form=form, filename=image)


@app.route('/linkedin_poster', methods=('GET', 'POST'))
def linkedin_poster():
    print("LinkedIn Poster...")
    title, post, image = retrieve_session()
    form = LinkedInPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        image = form.image.data

        print("Posting to LinkedIn...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        linkedin_api = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, "AccessToken")
        # TODO Extract this another method
        if image not in 'None':
            print(linkedin_api.publish_update(title + "\n" + post))

        else:
            print(linkedin_api.publish_update_with_image_attachment(title + "\n" + post,
                                                                    "", "",
                                                                    "",
                                                                    "",
                                                                    image))

        print("Redirecting...")
        return redirect('/next_poster' + "/linkedin")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/linkedin_post.html', form=form, filename=image)


@app.route('/tumblr_poster', methods=('GET', 'POST'))
def tumblr_poster():
    print("Tumblr Poster...")
    title, post, image = retrieve_session()
    form = TumblrPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        image = form.image.data

        print("Posting to Tumblr...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        tumblr_api = Tumblr(TUMBLR_CLIENT_ID,
                            TUMBLR_CLIENT_SECRET,
                            "AccessToken",
                            "AccessTokenSecret")

        if image not in 'None':
            tumblr_api.publish_update(
                body=post,
                title=title,
                blog_name="BlogName")

        else:
            tumblr_api.publish_update_with_image_attachment(
                caption=post,
                image_links=image,
                blog_name="BlogName")

        print("Redirecting...")
        return redirect('/next_poster' + "/tumblr")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/tumblr_post.html', form=form, filename=image)


@app.route('/next_poster/<done_soocialnetwork>')
def next_poster(done_soocialnetwork):
    done_soocialnetwork = done_soocialnetwork.strip()
    if str(done_soocialnetwork):
        print("Called next_poster/", done_soocialnetwork)
        try:
            social_networks = remove_session_socialnetwork(str(done_soocialnetwork))
            store_list_session(social_networks)
        except LookupError:
            pass
    social_networks = retrieve_session_socialnetworks()
    if social_networks:
        return redirect("/" + social_networks[0].lower() + "_poster")
    else:
        return redirect(url_for('post_status'))


@app.route('/post_status')
def post_status():
    # TODO Create separate page and display links to posted stuff or simply display success
    return "Done!"


@app.route('/dashboard')
def dashboard():
    stored_cookie = get_cookie(request)
    print("Stored Cookies:", stored_cookie)
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET, LINKEDIN_RETURN_URL)
    print(linkedin_auth.get_authorization_url())
    return render_template('dashboard/dashboard.html',
                           facebook_client_id=FACEBOOK_CLIENT_ID,
                           facebook_login="facebook_login",
                           linkedin_login=linkedin_auth.get_authorization_url(),
                           tumblr_login="tumblr_login",
                           twitter_login="twitter_login",
                           instagram_login=url_for('instagram_login'))


@app.route('/facebook_redirect')
def facebook_redirect():
    # We get this from dashboard.html as querystring
    access_token = request.args.get('accessToken')
    print("Facebook Access Token:", access_token)
    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, facebook_access_token=access_token)
    return resp


@app.route('/linkedin_redirect', methods=('GET', 'POST'))
def linkedin_redirect():
    # We get this from dashboard.html as querystring
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET,
                                 LINKEDIN_RETURN_URL
                                 )
    access_token = linkedin_auth.get_access_token_from_url(request.base_url)
    print("LinkedIn Access Token:", access_token)
    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, linkedin_access_token=access_token)
    return resp


@app.route('/instagram_login', methods=('GET', 'POST'))
def instagram_login():
    form = InstagramLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print("Instagram email:", email)
        print("Instagram password:", password)
        resp = make_response(redirect(url_for('dashboard')))
        resp = set_cookie(resp=resp, instagram_email=email, instagram_password=password)
        return resp
    return render_template('dashboard/instagram_login.html', form=form)


@app.route('/logout')
def logout():
    clear_session()


if __name__ == '__main__':
    app.run(debug=True)
