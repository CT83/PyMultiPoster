import os

from models.comon_queue.InstagramQueuer import InstagramQueuer

os.environ.setdefault('LC_TIME', 'en_GB')
# Don't change the position of this as this need to be set before the imports

import sys

from flask import Flask
from flask import render_template, url_for
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from CONSTANT import ON_HEROKU, AWS_RDS_URL, LOCALHOST_POSTGRES
from blueprints.administrator.Administrator import admin_blueprint
from blueprints.login.Login import get_current_user, login_blueprint
from blueprints.oauth_workflow.OAuthWorkflow import oauth_workflow
from blueprints.posters.Posters import posters
from models.Post import Post
from shared.models import db, login_manager
from table.models import PostTable

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "powerful secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "powerful secretkey"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager.init_app(app)
bootstrap = Bootstrap(app)

if not ON_HEROKU:
    print("Running on Local Environment...")
    os.chdir(sys.path[0])
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCALHOST_POSTGRES
else:
    print("Running on Heroku...")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_BINDS'] = {"common_queue": AWS_RDS_URL}

db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(login_blueprint)
app.register_blueprint(posters)
app.register_blueprint(admin_blueprint)
app.register_blueprint(oauth_workflow)
InstagramQueuer()


# Major
# TODO Add notification to remind user to sigin in to facebook accounts after few days to generate tokens
# TODO Move Images storage to S3
# TODO Setup different user levels to allow or prohibit users from signining in with their own accounts.

# Future
# TODO Move to MDBootstrap


# Minor
# TODO Add where to find company page id for linkedin
# TODO Add where to find page id for facebook
# TODO Replace {{wtf.quick_form(form)}} with proper HTML Formatted forms

@app.route('/')
def redirect_root():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('/home_page.html')


@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('redirect_root'))


@app.route('/user_posts')
@login_required
def user_posts():
    posts = Post.query.filter_by(user_email=get_current_user()).all()
    posts.reverse()  # Reverse Order of Posts
    for post in posts:
        post.no = posts.index(post) + 1
    table = PostTable(posts)
    return render_template('post/user_posts.html', table=table)


if __name__ == "__main__":
    app.run(debug=not ON_HEROKU, use_reloader=False)
