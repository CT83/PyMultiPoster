import datetime

from shared.models import db


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
