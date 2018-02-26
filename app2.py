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


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

person_one = Person(name='Test1')
person_two = Person(name='Test2')

pet_one = Pet(name='Spotty',owner=person_one)

db.session.add(person_one)
db.session.add(pet_one)
db.session.add(person_two)
db.session.commit()

if __name__ == '__main__':
    app.run()
