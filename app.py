import datetime
import os
import sys
from threading import Thread

from flask import Flask, render_template, url_for, request, make_response, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename, redirect

from CONSTANT import FACEBOOK_CLIENT_SECRET, FACEBOOK_CLIENT_ID, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, \
    LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, TUMBLR_CLIENT_SECRET, TUMBLR_CLIENT_ID, LINKEDIN_RETURN_URL, \
    TWITTER_REDIRECT_URL, TUMBLR_REDIRECT_URL, ON_HEROKU, UPLOAD_PATH, TWITTER_NAME, FACEBOOK_NAME, LINKEDIN_NAME, \
    TUMBLR_NAME, SUPPORTED_SOCIAL_NETWORKS
from Forms.FacebookPostForm import FacebookPostForm
from Forms.InstagramLoginForm import InstagramLoginForm
from Forms.InstagramPostForm import InstagramPostForm
from Forms.LinkedInPostForm import LinkedInPostForm
from Forms.LoginForm import LoginForm
from Forms.MainPostForm import MainPostForm
from Forms.SignupForm import SignupForm
from Forms.TumblrPostForm import TumblrPostForm
from Forms.TwitterPostForm import TwitterPostForm
from SocialMedia.Facebook.Facebook import Facebook
from SocialMedia.Instagram.Instagram import Instagram
from SocialMedia.LinkedIn.LinkedIn import LinkedIn, LinkedInAuth
from SocialMedia.Tumblr.Tumblr import Tumblr
from SocialMedia.Twitter.Twitter import Twitter
from cookie_management import set_cookie, get_cookie, get_signed_social
from session_management import save_session, retrieve_session, remove_session_socialnetwork, \
    store_list_session, retrieve_session_socialnetworks, clear_session
from table.models import PostTable, UsersTable

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "powerful secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "powerful secretkey"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)

if not ON_HEROKU:
    print("Running on Local Environment...")
    os.chdir(sys.path[0])
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:cybertech83@localhost/postgres"
else:
    print("Running on Heroku...")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)


# Major
# TODO Add some separate workflow for instagram
# TODO Add Admin View to see who posted what.
# TODO Shift Auth Keys to Database

class Users(db.Model):
    email = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))
    name = db.Column(db.Text)
    role = db.Column(db.Integer, default=1)  # Admin is level 10
    articles = db.relationship('Post', backref='user')

    def __init__(self, email, password, name, role=1):
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User {} {} {} {} {}>'.format(self.email, self.password, self.name, self.articles,
                                              self.role)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    def promote_to_admin(self):
        self.role = 10

    def is_admin(self):
        if self.role is not None:
            return self.role >= 10
        else:
            return False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    image = db.Column(db.Text)
    social_network = db.Column(db.Text)
    date_posted = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_email = db.Column(db.String(80), db.ForeignKey('users.email'))

    def __repr__(self):
        return '<Post:{} {} {} {} {} {} {}>' \
            .format(self.id, self.title, self.content, self.image,
                    self.social_network, self.user_email,
                    self.date_posted)


# TODO Change image Aspect Ratio to fit instagram
# TODO Add Quick Post button
def is_string_empty(s):
    return str(s) in 'None' or str(s) in "" or s is None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Users.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = Users(form.email.data, form.password.data, form.name.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return redirect(url_for('login'))
        else:
            return "Form didn't validate"


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()


@app.route('/protected')
@login_required
def protected():
    return "protected area"


@login_manager.user_loader
def load_user(email):
    return Users.query.filter_by(email=email).first()


def get_current_user():
    from flask_login import current_user
    if current_user.is_authenticated():
        return current_user.email
    else:
        return None


def insert_post_current_user(content, social_network, db, image="", title="",
                             user=None):
    if user is None:
        user = load_user(get_current_user())

    import datetime
    time_indian = datetime.datetime.utcnow()
    time_indian = time_indian + datetime.timedelta(hours=5, minutes=30)

    post = Post(title=title, content=content, social_network=social_network, image=image,
                user=user, date_posted=time_indian)
    db.session.add(post)
    db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # TODO Change to validate_on_submit
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    return "Wrong password!"
            else:
                return "user doesn't exist!"
    else:
        return "form not validated"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    clear_session()
    return redirect_root()


@app.route('/main', methods=('GET', 'POST'))
@login_required
def main():
    # TODO Determine which social networks are linked and display checkboxes only for them.

    form = MainPostForm()
    signed_social = get_signed_social(request)
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


@app.route('/facebook_poster', methods=('GET', 'POST'))
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

        stored_cookie = get_cookie(request)
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
                                 social_network=FACEBOOK_NAME, db=db)

        print("Redirecting...")
        return redirect('/next_poster' + "/facebook")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/facebook_post.html', form=form, filename=image)


@app.route('/twitter_poster', methods=('GET', 'POST'))
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

        stored_cookie = get_cookie(request)
        twitter_api = Twitter(TWITTER_CLIENT_ID,
                              TWITTER_CLIENT_SECRET,
                              stored_cookie['twitter_access_token'],
                              stored_cookie['twitter_access_secret'])

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
        insert_post_current_user(content=post, image=image, social_network=TWITTER_NAME, db=db)
        print("Redirecting...")
        return redirect('/next_poster' + "/twitter")
    else:
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/twitter_post.html', form=form, filename=image)


@app.route('/instagram_poster', methods=('GET', 'POST'))
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
        # TODO Add allow uploading if no image is selected

        stored_cookie = get_cookie(request)

        instagram_api = Instagram(stored_cookie['instagram_email'],
                                  stored_cookie['instagram_password'])
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


@app.route('/linkedin_poster', methods=('GET', 'POST'))
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

        stored_cookie = get_cookie(request)
        linkedin_api = LinkedIn(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET,
                                stored_cookie['linkedin_access_token'])
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
                                 social_network=LINKEDIN_NAME, db=db)
        print("Redirecting...")
        return redirect('/next_poster' + "/linkedin")
    else:
        form.title.data = title
        form.post.data = post
        form.image.data = image
        form.image.render_kw = {'disabled': 'disabled'}

    return render_template('post/linkedin_post.html', form=form, filename=image)


@app.route('/tumblr_poster', methods=('GET', 'POST'))
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
                                 social_network=TUMBLR_NAME, db=db)
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


@app.route('/next_poster/<done_socialnetwork>')
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
        return redirect(url_for('post_status'))


@app.route('/post_status')
@login_required
def post_status():
    # TODO Create separate page and display links to posted stuff or simply display success
    data = get_current_posts_with_links()
    clear_current_posts()
    return render_template('post/done_post.html', data=data)


@app.route('/dashboard')
@login_required
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
@login_required
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
@login_required
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
@login_required
def instagram_login():
    # TODO Check instagram password on the server
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
@login_required
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
@login_required
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


@app.route('/')
def redirect_root():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('/home_page.html')


@app.route('/temp')
@login_required
def temp():
    for user in Users.query.all():
        print(user)
    for post in Post.query.all():
        print(post)
    return render_template('temp.html')


@app.route('/admin_signup', methods=('GET', 'POST'))
# TODO Make Admin Signup more secured
def admin_signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('admin/admin_signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Users.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = Users(form.email.data, form.password.data, form.name.data, role=10)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return "Signed Up successfully as Admin"
        else:
            return "Form didn't validate"


@app.route('/admin_view')
@login_required
def admin_view():
    return "Admin View"


@app.route('/admin_view_users')
@login_required
# TODO Create a @admin_required decorator to manage admin only views.
# TODO Lock this down.
def admin_view_users():
    users = Users.query.all()
    for user in users:
        user.link = user.email
    table = UsersTable(users)
    print(table.__html__())
    return render_template('admin/view_users.html', table=table)


@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('redirect_root'))


@app.route('/admin_user_posts')
@login_required
# TODO Add admin required decorator here
# DRY This function with user_posts
def admin_user_posts():
    user = request.args.get('id')
    print(request.args)
    print(user)
    posts = Post.query.filter_by(user_email=user).all()
    posts.reverse()  # Reverse Order of Posts
    table = PostTable(posts)
    return render_template('post/user_posts.html', table=table)


@app.route('/user_posts')
@login_required
def user_posts():
    posts = Post.query.filter_by(user_email=get_current_user()).all()
    posts.reverse()  # Reverse Order of Posts
    table = PostTable(posts)
    return render_template('post/user_posts.html', table=table)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
