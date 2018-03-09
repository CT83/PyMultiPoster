from app import db


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_access_token = db.Column(db.Text)
    twitter_access_token = db.Column(db.Text)
    twitter_access_secret = db.Column(db.Text)
    instagram_email = db.Column(db.Text)
    instagram_password = db.Column(db.Text)
    linkedin_access_token = db.Column(db.Text)
    tumblr_access_token = db.Column(db.Text)
    tumblr_access_secret = db.Column(db.Text)

    user_email = db.Column(db.String(80), db.ForeignKey('users.email'))

    def __repr__(self):
        return '<Credentials:{}>'.format(self.id)
