import os
from flask import render_template, request, Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:cybertech83@localhost/postgres"


# TODO Split file into multiple BluePrints

@app.route('/facebook_login')
def facebook_login():
    return render_template('facebook_login.html', app_id='101206834030831')


def post_to_instagram():
    from InstagramAPI import InstagramAPI
    InstagramAPI = InstagramAPI("pyreserver.pseudtech@gmail.com", "cybertech83")
    InstagramAPI.login()  # login

    photo_path = 'temp.jpg'
    caption = "Sample photo"
    InstagramAPI.uploadPhoto(photo_path, caption=caption)


@app.route('/instagram_login')
def instagram_login():
    post_to_instagram()
    return render_template('instagram_login.html', app_id='101206834030831')


@app.route('/blogger_login')
def blogger_login():
    return render_template('blogger_login.html',
                           api_key='AIzaSyCSnqsAMqjwGVMeykY59UgWEsYfNlRuFYg',
                           app_id='812327379487-4mmbsmmnefh3986ogca7qhb8ihqtillh.apps.googleusercontent.com')


@app.route('/blogger_redirect')
def blogger_redirect():
    return "Redirected to blogger_redirect"


@app.route('/twitter_redirect')
def twitter_redirect():
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('oauth_token')
    print("OAuthToken Twitter:" + user)
    return "Redirected to twitter_redirect"


@app.route('/')
def homepage():
    return render_template('home.html', app_id='101206834030831')


@app.route('/google91e934bee0a01da8.html')
def google91e934bee0a01da8():
    return render_template('google91e934bee0a01da8.html')


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class Example(db.Model):
    __tablename__ = 'example'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)


user = User('Jo2hn D2oe', 'john.2deoe@example.com')
db.session.add(user)
db.session.commit()
print(User.query.all())

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
