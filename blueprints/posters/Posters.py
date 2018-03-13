from threading import Thread

from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from CONSTANT import UPLOAD_PATH, FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, FACEBOOK_NAME, TWITTER_CLIENT_ID, \
    TWITTER_CLIENT_SECRET, TWITTER_NAME, LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_NAME, TUMBLR_CLIENT_ID, \
    TUMBLR_CLIENT_SECRET, TUMBLR_NAME, SUPPORTED_SOCIAL_NETWORKS
from Forms.FacebookPostForm import FacebookPostForm
from Forms.InstagramPostForm import InstagramPostForm
from Forms.LinkedInPostForm import LinkedInPostForm
from Forms.MainPostForm import MainPostForm
from Forms.TumblrPostForm import TumblrPostForm
from Forms.TwitterPostForm import TwitterPostForm
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.Instagram.Instagram import Instagram
from SocialMedia.LinkedIn.LinkedIn import LinkedIn
from SocialMedia.Tumblr.Tumblr import Tumblr
from SocialMedia.Twitter.Twitter import Twitter
from blueprints.login.Login import get_current_user
from models.Credentials import get_credentials
from models.Post import insert_post_current_user
from shared.models import db
from utils.MiscUtils import get_signed_social
from utils.StringUtils import is_string_empty
from utils.session_management import save_session, retrieve_session, remove_session_socialnetwork, store_list_session, \
    retrieve_session_socialnetworks

posters = Blueprint('Posters', __name__)


@posters.route('/main', methods=('GET', 'POST'))
@login_required
def main():
    form = MainPostForm()
    signed_social = get_signed_social(get_current_user())
    form.selected_socialnetworks.choices = [(x, x) for x in signed_social]

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        social_networks = form.selected_socialnetworks.data
        try:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(UPLOAD_PATH + filename)
            filename = UPLOAD_PATH + filename
        except AttributeError:
            filename = ""
        print("main() Submitted Form...")
        print("Title:", title)
        print("Post:", post)
        print("Social Networks:", social_networks)
        print("Image:", filename)
        save_session(filename, post, title, social_networks)
        print("Redirecting...")
        return redirect('/next_poster/main')
    return render_template('post/main.html', form=form, )


@posters.route('/facebook_poster', methods=('GET', 'POST'))
@login_required
def facebook_poster():
    print("Facebook Poster...")
    print("Logged in as", get_current_user())

    title, post, image = retrieve_session()
    form = FacebookPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        page_id = form.page_id.data

        print("Posting to Facebook...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)
        print("Page ID:", page_id)

        # stored_cookie = get_cookie(request)
        stored_cookie = get_credentials(get_current_user())
        facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                                 FACEBOOK_CLIENT_SECRET,
                                 stored_cookie['facebook_access_token'])
        thread = Thread()
        if is_string_empty(image) and is_string_empty(page_id):
            print("Posting to Wall...")
            thread = Thread(target=facebook_user.publish_update,
                            kwargs=dict(message=title + "\n" + post))

        if is_string_empty(image) and not is_string_empty(page_id):
            print("Posting to Page...")
            thread = Thread(target=facebook_user.publish_update_page,
                            kwargs=dict(message=title + "\n" + post,
                                        page_id=page_id))

        if not is_string_empty(image) and is_string_empty(page_id):
            print("Posting to Wall with Image...")
            thread = Thread(target=facebook_user.publish_update_image,
                            kwargs=dict(message=title + "\n" + post,
                                        image=image))

        if not is_string_empty(image) and not is_string_empty(page_id):
            print("Posting to Page with Image...")
            thread = Thread(target=facebook_user.publish_update_image_page,
                            kwargs=dict(message=title + "\n" + post,
                                        page_id=page_id,
                                        image=image))
        thread.start()
        thread.join()
        session[FACEBOOK_NAME + '_POST_URL'] = facebook_user.get_link_latest_post()

        insert_post_current_user(title=title, content=post, image=image,
                                 social_network=FACEBOOK_NAME,
                                 link=facebook_user.get_link_latest_post(),
                                 db=db)

        print("Redirecting...")
        return redirect('/next_poster' + "/facebook")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/facebook_post.html', form=form, filename=image)


@posters.route('/twitter_poster', methods=('GET', 'POST'))
@login_required
def twitter_poster():
    print("Twitter Poster...")
    _, post, image = retrieve_session()
    form = TwitterPostForm()
    if form.validate_on_submit():
        post = form.post.data

        print("Posting to Twitter...")
        print("Post:", post)
        print("Image:", image)

        # stored_c = get_cookie(request)
        stored_c = get_credentials(get_current_user())
        twitter_api = Twitter(TWITTER_CLIENT_ID,
                              TWITTER_CLIENT_SECRET,
                              stored_c['twitter_access_token'],
                              stored_c['twitter_access_secret'])

        if is_string_empty(image):
            # print(twitter_api.publish_update(post))
            thread = Thread(target=twitter_api.publish_update,
                            kwargs=dict(message=post))
        else:
            # print(twitter_api.publish_update_with_image_attachment(post, image))
            thread = Thread(target=twitter_api.publish_update_with_image_attachment,
                            kwargs=dict(message=post,
                                        image_url=image))
        thread.start()
        thread.join()
        session[TWITTER_NAME + '_POST_URL'] = twitter_api.get_link_latest_post()
        insert_post_current_user(content=post, image=image, social_network=TWITTER_NAME,
                                 link=twitter_api.get_link_latest_post(), db=db)
        print("Redirecting...")
        return redirect('/next_poster' + "/twitter")
    else:
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/twitter_post.html', form=form, filename=image)


@posters.route('/instagram_poster', methods=('GET', 'POST'))
@login_required
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

        # stored_c = get_cookie(request)
        stored_c = get_credentials(get_current_user())

        instagram_api = Instagram(stored_c['instagram_email'],
                                  stored_c['instagram_password'])
        # jpg_image = instagram_api.convert_image_to_compatible_format(image)
        Thread(target=instagram_api.convert_publish_update_with_image_attachment,
               kwargs=dict(message=post,
                           image_url=image)).start()

        # instagram_api.cleanup()

        insert_post_current_user(content=post, image=image, social_network=TWITTER_NAME, db=db)

        print("Redirecting...")
        return redirect('/next_poster' + "/instagram")
    else:
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/instagram_post.html', form=form, filename=image)


@posters.route('/linkedin_poster', methods=('GET', 'POST'))
@login_required
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

        # stored_c = get_cookie(request)
        stored_c = get_credentials(get_current_user())
        linkedin_api = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET,
                                stored_c['linkedin_access_token'])
        if is_string_empty(image):
            thread = Thread(target=linkedin_api.publish_update,
                            kwargs=dict(title=title, message=post))
        else:
            thread = Thread(target=linkedin_api.upload_publish_image,
                            kwargs=dict(title=title,
                                        message=post,
                                        image_url=image))

        thread.start()
        thread.join()
        session[LINKEDIN_NAME + '_POST_URL'] = linkedin_api.get_link_latest_post()

        insert_post_current_user(title=title, content=post, image=image,
                                 social_network=LINKEDIN_NAME,
                                 link=linkedin_api.get_link_latest_post(),
                                 db=db)
        print("Redirecting...")
        return redirect('/next_poster' + "/linkedin")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/linkedin_post.html', form=form, filename=image)


@posters.route('/tumblr_poster', methods=('GET', 'POST'))
@login_required
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
        # print("Image:", image)
        # stored_c = get_cookie(request)
        stored_c = get_credentials(get_current_user())
        tumblr_api = Tumblr(TUMBLR_CLIENT_ID,
                            TUMBLR_CLIENT_SECRET,
                            stored_c['tumblr_access_token'],
                            stored_c['tumblr_access_secret'])

        if is_string_empty(title):
            title = 'PyMultiPoster'

        if str(image) in 'None' or str(image) in '' or image is None:
            thread = Thread(target=tumblr_api.publish_update,
                            kwargs=dict(message=post, title=title, blog_name=blog_name))
        else:
            thread = Thread(target=tumblr_api.publish_update_with_image_attachment,
                            kwargs=dict(caption=post, image_links=image,
                                        blog_name=blog_name))

        thread.start()
        thread.join()
        session[TUMBLR_NAME + '_POST_URL'] = tumblr_api.get_link_latest_post()

        insert_post_current_user(title=title, content=post, image=image,
                                 social_network=TUMBLR_NAME,
                                 link=tumblr_api.get_link_latest_post(),
                                 db=db)
        return redirect('/next_poster' + "/tumblr")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/tumblr_post.html', form=form, filename=image)


def get_current_posts_with_links(networks=SUPPORTED_SOCIAL_NETWORKS):
    posts_links = []
    for network in networks:
        try:
            posts_links.append([network, session[network + '_POST_URL']])
        except LookupError:
            pass
    print("Current Post Links", posts_links)
    return posts_links


def clear_current_posts(networks=SUPPORTED_SOCIAL_NETWORKS):
    for network in networks:
        try:
            session.pop(network + '_POST_URL')
        except LookupError:
            pass


@posters.route('/next_poster/<done_socialnetwork>')
@login_required
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
        return redirect(url_for('Posters.post_status'))


@posters.route('/post_status')
@login_required
def post_status():
    data = get_current_posts_with_links()
    clear_current_posts()
    return render_template('post/done_post.html', data=data)


@posters.route('/view_post')
@login_required
def view_post():
    from flask import request
    redirect_url = request.args.get('url')
    return redirect(redirect_url)
