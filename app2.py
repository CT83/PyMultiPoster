import os

from flask import render_template, Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from CONSTANT import ON_HEROKU

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if ON_HEROKU:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:cybertech83@localhost/postgres"


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
    provider = db.Column(db.String(120))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class Example(db.Model):
    __tablename__ = 'example'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)
    test = db.Column('test', db.String)


user = User('Jo2hn Doe4', 'john.deoe3@example.com')
db.session.add(user)
db.session.commit()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run()
    manager.run()
