from threading import Thread

from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from CONSTANT import UPLOAD_PATH, FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, FACEBOOK_NAME, TWITTER_CLIENT_ID, \
    TWITTER_CLIENT_SECRET, TWITTER_NAME, LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_NAME, TUMBLR_CLIENT_ID, \
    TUMBLR_CLIENT_SECRET, TUMBLR_NAME, SUPPORTED_SOCIAL_NETWORKS, INSTAGRAM_NAME, S3_BUCKET, S3_KEY, S3_SECRET
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
from aws.aws_S3 import S3
from blueprints.login.Login import get_current_user
from models.Credentials import get_credentials
from models.Post import insert_post_current_user
from shared.models import db
from utils.FileUtils import rename_file, get_file_extension, get_filename_from_url
from utils.MiscUtils import get_signed_social, get_random_string
from utils.StringUtils import is_string_empty, is_string_populated
from utils.SessionUtils import save_session, retrieve_session, remove_session_socialnetwork, store_list_session, \
    retrieve_session_socialnetworks, clear_session

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

            image_path = "".join([UPLOAD_PATH,
                                  get_random_string(),
                                  get_file_extension(filename)])
            print("Randomized Image Path:", image_path)

            rename_file(old=filename, new=image_path)
            filename = image_path

            # TODO Retrieve the images completely from S3 in the future instead of just storing them there for Log purposes
            s3 = S3(bucket=S3_BUCKET, key=S3_KEY, secret=S3_SECRET)
            image_s3_url = s3.upload(open(filename, 'rb'),
                                     destination_filename="uploads/"
                                                          + get_filename_from_url(filename))
            print("S3 Image URL:", image_s3_url)

        except AttributeError:
            filename = ""
            image_s3_url = None
        print("main() Submitted Form...")
        print("Title:", title)
        print("Post:", post)
        print("Social Networks:", social_networks)
        print("Image:", filename)
        save_session(filename, post, title, social_networks, image_url=image_s3_url)
        print("Redirecting...")
        return redirect('/next_poster/main')
    return render_template('post/main.html', form=form, )


@posters.route('/facebook_poster', methods=('GET', 'POST'))
@login_required
def facebook_poster():
    print("Facebook Poster...")
    print("Logged in as", get_current_user())

    title, post, _ = retrieve_session()
    image_url = session["image_url"]

    form = FacebookPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        page_id = form.page_id.data

        print("Posting to Facebook...")
        print("Title:", title)
        print("Post:", post)
        print("Image URL:", image_url)
        print("Page ID:", page_id)

        stored_cred = get_credentials(get_current_user())
        facebook_user = Facebook(FACEBOOK_CLIENT_ID,
                                 FACEBOOK_CLIENT_SECRET,
                                 stored_cred['facebook_access_token'])
        thread = Thread()
        if is_string_empty(image_url) and is_string_empty(page_id):
            print("Posting to Wall...")
            thread = Thread(target=facebook_user.publish_update,
                            kwargs=dict(message=title + "\n" + post))

        if is_string_empty(image_url) and not is_string_empty(page_id):
            print("Posting to Page...")
            thread = Thread(target=facebook_user.publish_update_page,
                            kwargs=dict(message=title + "\n" + post,
                                        page_id=page_id))

        if not is_string_empty(image_url) and is_string_empty(page_id):
            print("Posting to Wall with Image...")
            thread = Thread(target=facebook_user.publish_update_image,
                            kwargs=dict(message=title + "\n" + post,
                                        image_url=image_url))

        if not is_string_empty(image_url) and not is_string_empty(page_id):
            print("Posting to Page with Image...")
            thread = Thread(target=facebook_user.publish_update_image_page,
                            kwargs=dict(message=title + "\n" + post,
                                        page_id=page_id,
                                        image_url=image_url))
        thread.start()
        thread.join()
        session[FACEBOOK_NAME + '_POST_URL'] = facebook_user.get_link_latest_post()

        insert_post_current_user(title=title, content=post, image_url=image_url,
                                 social_network=FACEBOOK_NAME,
                                 link=facebook_user.get_link_latest_post(),
                                 db=db)

        return redirect('/next_poster' + "/facebook")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image_url
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/facebook_post.html', form=form, filename=image_url)


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

        stored_c = get_credentials(get_current_user())
        twitter_api = Twitter(TWITTER_CLIENT_ID,
                              TWITTER_CLIENT_SECRET,
                              stored_c['twitter_access_token'],
                              stored_c['twitter_access_secret'])

        if is_string_empty(image):
            thread = Thread(target=twitter_api.publish_update,
                            kwargs=dict(message=post))
        else:
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
    _, post, _ = retrieve_session()
    image = session["image_url"]
    form = InstagramPostForm()
    if form.validate_on_submit():
        post = form.post.data

        print("Posting to Instagram...")
        print("Post:", post)
        print("Image:", image)

        instagram_api = Instagram()
        instagram_api.publish_update_image(message=post, image=image,
                                           db_session=db.session,
                                           user_email=get_current_user())

        session[INSTAGRAM_NAME + '_POST_URL'] = "#"
        insert_post_current_user(content=post, image=image,
                                 social_network=INSTAGRAM_NAME,
                                 db=db)

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
    image_url = session["image_url"]
    image = image_url
    form = LinkedInPostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        # image = form.image.data
        page_id = form.page_id.data

        print("Posting to LinkedIn...")
        print("Title:", title)
        print("Post:", post)
        print("Image:", image)

        stored_c = get_credentials(get_current_user())
        linkedin_api = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET,
                                stored_c['linkedin_access_token'])
        if is_string_populated(page_id):
            if is_string_empty(image):
                print("Posting message to Company Page, LinkedIn")
                thread = Thread(target=linkedin_api.publish_update_company_page,
                                kwargs=dict(title=title, message=post,
                                            company_id=page_id))
            else:
                print("Posting Image to Company Page, LinkedIn")
                thread = Thread(target=linkedin_api.publish_update_company_page,
                                kwargs=dict(title=title, message=post,
                                            company_id=page_id,
                                            submitted_url=image_url,
                                            submitted_image_url=image_url))

        else:
            if is_string_empty(image):
                print("Posting message, LinkedIn")
                thread = Thread(target=linkedin_api.publish_update,
                                kwargs=dict(title=title, message=post))
            else:
                print("Posting Image, LinkedIn")
                thread = Thread(target=linkedin_api.publish_update_with_image_attachment,
                                kwargs=dict(title=title, message=post,
                                            image_url=image_url,
                                            link_att=image_url))

        thread.start()
        thread.join()
        session[LINKEDIN_NAME + '_POST_URL'] = linkedin_api.get_link_latest_post()

        insert_post_current_user(title=title, content=post, image=image_url,
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

        print("Posting to Tumblr...")
        print("Title:", title)
        print("Post:", post)
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
        clear_session()
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
    if redirect_url:
        return redirect(redirect_url)
    else:
        return ('', 204)
