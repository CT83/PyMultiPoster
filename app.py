import os
import sys
from threading import Thread

from flask import Flask, render_template, url_for, request, make_response
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename, redirect

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, \
    LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, TUMBLR_CLIENT_SECRET, TUMBLR_CLIENT_ID, LINKEDIN_RETURN_URL, \
    TWITTER_REDIRECT_URL, TUMBLR_REDIRECT_URL, IMGUR_CLIENT_ID, ON_HEROKU, UPLOAD_PATH
from Forms.FacebookPostForm import FacebookPostForm
from Forms.InstagramLoginForm import InstagramLoginForm
from Forms.InstagramPostForm import InstagramPostForm
from Forms.LinkedInPostForm import LinkedInPostForm
from Forms.MainPostForm import MainPostForm
from Forms.TumblrPostForm import TumblrPostForm
from Forms.TwitterPostForm import TwitterPostForm
from Imgur.Imgur import upload_to_imgur
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.Instagram.Instagram import Instagram
from SocialMedia.LinkedIn.LinkedIn import LinkedIn, LinkedInAuth
from SocialMedia.Tumblr.Tumblr import Tumblr
from SocialMedia.Twitter.Twitter import Twitter
from cookie_management import set_cookie, get_cookie
from session_management import clear_session, save_session, retrieve_session, remove_session_socialnetwork, \
    store_list_session, retrieve_session_socialnetworks

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "powerful secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "powerful secretkey"
bootstrap = Bootstrap(app)

if not ON_HEROKU:
    os.chdir(sys.path[0])


# TODO Change image Aspect Ratio to fit instagram
# TODO Implement Polymorphism perfectly for Social Media Networks
# TODO Add Posters to their own independent threads
def is_string_empty(s):
    return str(s) in 'None' or str(s) in "" or s is None


@app.route('/main', methods=('GET', 'POST'))
def main():
    form = MainPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        social_networks = form.selected_socialnetworks.data
        try:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(UPLOAD_PATH + filename)
            filename = UPLOAD_PATH + filename
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

        print("Posting to Facebook...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        stored_cookie = get_cookie(request)
        facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                                 FACEBOOK_CLIENT_SECRET,
                                 stored_cookie['facebook_access_token'])
        if is_string_empty(image):
            Thread(target=facebook_user.publish_update, args=(title + "\n" + post)).start()
        else:
            # image_url = upload_to_imgur(IMGUR_CLIENT_ID, image)
            # facebook_user.publish_update_with_image_attachment(message=title + "\n" + post,
            #                                                    image_url=image_url)
            Thread(target=facebook_user.convert_publish_update_with_image_attachment,
                   kwargs=dict(message=title + "\n" + post,
                               image_url=image)).start()

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
    _, post, image = retrieve_session()
    form = TwitterPostForm()
    if form.validate_on_submit():
        post = form.post.data

        print("Posting to Twitter...")
        print("Post:", post)
        print("Image:", image)

        stored_cookie = get_cookie(request)
        twitter_api = Twitter(TWITTER_CLIENT_ID,
                              TWITTER_CLIENT_SECRET,
                              stored_cookie['twitter_access_token'],
                              stored_cookie['twitter_access_secret'])

        if is_string_empty(image):
            # print(twitter_api.publish_update(post))
            Thread(target=twitter_api.publish_update,
                   kwargs=dict(message=post)).start()
        else:
            # print(twitter_api.publish_update_with_image_attachment(post, image))
            Thread(target=twitter_api.publish_update_with_image_attachment,
                   kwargs=dict(message=post,
                               image_url=image)).start()
        print("Redirecting...")
        return redirect('/next_poster' + "/twitter")
    else:
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/twitter_post.html', form=form, filename=image)


@app.route('/instagram_poster', methods=('GET', 'POST'))
def instagram_poster():
    print("Instagram Poster...")
    _, post, image = retrieve_session()
    form = InstagramPostForm()
    if form.validate_on_submit():
        post = form.post.data
        # image = form.image.data

        print("Posting to Instagram...")
        print("Post:", post)
        print("Image:", image)
        # TODO Add allow uploading if no image is selected

        stored_cookie = get_cookie(request)

        instagram_api = Instagram(stored_cookie['instagram_email'],
                                  stored_cookie['instagram_password'])
        # jpg_image = instagram_api.convert_image_to_compatible_format(image)
        Thread(target=instagram_api.convert_publish_update_with_image_attachment,
               kwargs=dict(message=post,
                           image_url=image)).start()

        # instagram_api.cleanup()

        print("Redirecting...")
        return redirect('/next_poster' + "/instagram")
    else:
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
        # image = form.image.data

        print("Posting to LinkedIn...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        stored_cookie = get_cookie(request)
        linkedin_api = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET,
                                stored_cookie['linkedin_access_token'])
        if is_string_empty(image):
            # print(linkedin_api.publish_update(title=title, message=post))
            Thread(target=linkedin_api.publish_update,
                   kwargs=dict(title=title, message=post)).start()
        else:
            # image_url = upload_to_imgur(IMGUR_CLIENT_ID, image)
            # print(
            #     linkedin_api.publish_update_with_image_attachment(title=title,
            #                                                       message=post,
            #                                                       image_url=image_url))
            Thread(target=linkedin_api.convert_publish_update_with_image_attachment,
                   kwargs=dict(title=title,
                               message=post,
                               image_url=image)).start()

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
        blog_name = form.blog_name.data
        # image = form.image.data

        print("Posting to Tumblr...")
        print("Title:", title)
        print("Post:", post)
        # TODO Look into how titles and hashtags are managed for all social network posters
        # print("Image:", image)
        stored_cookie = get_cookie(request)
        tumblr_api = Tumblr(TUMBLR_CLIENT_ID,
                            TUMBLR_CLIENT_SECRET,
                            stored_cookie['tumblr_access_token'],
                            stored_cookie['tumblr_access_secret'])

        if is_string_empty(title):
            title = 'PyMultiPoster'

        if str(image) in 'None' or str(image) in '' or image is None:
            # tumblr_api.publish_update(
            #     message=post,
            #     title=title,
            #     blog_name=blog_name)
            Thread(target=tumblr_api.publish_update,
                   kwargs=dict(message=post, title=title, blog_name=blog_name)).start()
        else:
            # tumblr_api.publish_update_with_image_attachment(
            #     caption=post,
            #     image_links=image,
            #     blog_name=blog_name)
            Thread(target=tumblr_api.publish_update_with_image_attachment,
                   kwargs=dict(caption=post, image_links=image,
                               blog_name=blog_name)).start()

        return redirect('/next_poster' + "/tumblr")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/tumblr_post.html', form=form, filename=image)


@app.route('/next_poster/<done_socialnetwork>')
def next_poster(done_socialnetwork):
    done_socialnetwork = done_socialnetwork.strip()
    if str(done_socialnetwork):
        print("Called next_poster/", done_socialnetwork)
        try:
            social_networks = remove_session_socialnetwork(str(done_socialnetwork))
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

    from flask import session
    from SocialMedia.Twitter import TwitterAuth
    twitter_auth_url, key, secret \
        = TwitterAuth.get_authorization_url_auth(TWITTER_CLIENT_ID,
                                                 TWITTER_CLIENT_SECRET,
                                                 TWITTER_REDIRECT_URL)
    session['twitter_request_token'] = (key, secret)

    from SocialMedia.Tumblr.TumblrAuth import get_authorization_url
    tum_url, tum_key, tum_sec = get_authorization_url(TUMBLR_CLIENT_ID,
                                                      TUMBLR_CLIENT_SECRET,
                                                      TUMBLR_REDIRECT_URL)
    session['tumblr_request_token'] = (tum_key, tum_sec)

    return render_template('dashboard/dashboard.html',
                           facebook_client_id=FACEBOOK_CLIENT_ID,
                           linkedin_login=linkedin_auth.get_authorization_url(),
                           tumblr_login=tum_url,
                           twitter_login=twitter_auth_url,
                           instagram_login=url_for('instagram_login'))


@app.route('/facebook_redirect')
def facebook_redirect():
    # We get this from dashboard.html as querystring
    access_token = request.args.get('accessToken')
    print("Facebook Access Token:", access_token)
    facebook_api = Facebook(FACEBOOK_CLIENT_ID,
                            FACEBOOK_CLIENT_SECRET,
                            access_token)
    access_token = facebook_api.generate_long_lived_token()
    print("Facebook Long Lived Access Token:", access_token)

    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, facebook_access_token=access_token)
    return resp


@app.route('/linkedin_redirect', methods=('GET', 'POST'))
def linkedin_redirect():
    # We get this from dashboard.html as querystring
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID,
                                 LINKEDIN_CLIENT_SECRET,
                                 LINKEDIN_RETURN_URL)
    access_token = linkedin_auth.get_access_token_from_url(request.url)
    print("LinkedIn Access Token:", access_token)
    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, linkedin_access_token=access_token)
    return resp


@app.route('/instagram_login', methods=('GET', 'POST'))
def instagram_login():
    form = InstagramLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("Instagram Username:", username)
        print("Instagram Password:", password)
        resp = make_response(redirect(url_for('dashboard')))
        resp = set_cookie(resp=resp, instagram_email=username, instagram_password=password)
        return resp
    return render_template('dashboard/instagram_login.html', form=form)


@app.route('/twitter_redirect', methods=('GET', 'POST'))
def twitter_redirect():
    from flask import session
    from SocialMedia.Twitter.TwitterAuth import get_access_token_from_url

    token = session['twitter_request_token']
    del session['twitter_request_token']

    access_token, access_token_secret = \
        get_access_token_from_url(response_url=request.url,
                                  consumer_key=TWITTER_CLIENT_ID,
                                  consumer_secret=TWITTER_CLIENT_SECRET,
                                  token=token)

    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, twitter_access_token=access_token,
                      twitter_access_secret=access_token_secret)
    return resp


@app.route('/tumblr_redirect', methods=('GET', 'POST'))
def tumblr_redirect():
    from flask import session

    sess = session['tumblr_request_token']
    res_key = sess[0]
    res_sec = sess[1]
    del session['tumblr_request_token']

    from SocialMedia.Tumblr.TumblrAuth import get_access_token_from_url
    tokens = get_access_token_from_url(TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET,
                                       res_key, res_sec,
                                       request.url,
                                       callback_url=TUMBLR_REDIRECT_URL)

    print(tokens)
    resp = make_response(redirect(url_for('dashboard')))
    resp = set_cookie(resp=resp, tumblr_access_token=tokens['oauth_token'],
                      tumblr_access_secret=tokens['oauth_token_secret'])

    return resp


@app.route('/logout')
def logout():
    clear_session()


if __name__ == '__main__':
    app.run(debug=True)
