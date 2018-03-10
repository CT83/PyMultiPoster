from shared.models import db


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

    # TODO Define Repr here

    def save_credential_to_db(self, dictionary):
        user_email = self.user_email
        cred = Credentials.query.filter_by(user_email=user_email).update(dictionary)
        db.session.commit()


def save_credentials(username, facebook_access_token="", twitter_access_token="",
                     twitter_access_secret="", instagram_email="", instagram_password="",
                     linkedin_access_token="", tumblr_access_token="",
                     tumblr_access_secret=""):
    if facebook_access_token:
        print("Saving Facebook Credentials to DB")
        cred = Credentials(user_email=username,
                           facebook_access_token=facebook_access_token)
        cred.save_credential_to_db(dict(facebook_access_token=facebook_access_token))

    if twitter_access_token and twitter_access_secret:
        print("Saving Twitter Credentials to DB")
        cred = Credentials(user_email=username,
                           twitter_access_token=twitter_access_token,
                           twitter_access_secret=twitter_access_secret)
        cred.save_credential_to_db(dict(twitter_access_token=twitter_access_token,
                                        twitter_access_secret=twitter_access_secret))

    if instagram_email and instagram_password:
        print("Saving Instagram Credentials to DB")
        cred = Credentials(user_email=username,
                           instagram_email=instagram_email,
                           instagram_password=instagram_password)
        cred.save_credential_to_db(dict(instagram_email=instagram_email,
                                        instagram_password=instagram_password))

    if linkedin_access_token:
        print("Saving Linkedin Credentials to DB")
        cred = Credentials(user_email=username,
                           linkedin_access_token=linkedin_access_token)
        cred.save_credential_to_db(dict(linkedin_access_token=linkedin_access_token))

    if tumblr_access_token and tumblr_access_secret:
        print("Saving Tumblr Credentials to DB")
        cred = Credentials(user_email=username,
                           tumblr_access_token=tumblr_access_token,
                           tumblr_access_secret=tumblr_access_secret)
        cred.save_credential_to_db(dict(tumblr_access_token=tumblr_access_token,
                                        tumblr_access_secret=tumblr_access_secret))


def get_credentials(username):
    c = Credentials()
    try:
        c = Credentials.query.filter_by(user_email=username).first()
    except:
        pass

    credentials = {'facebook_access_token': getattr(c, 'facebook_access_token', None),
                   'twitter_access_token': getattr(c, 'twitter_access_token', None),
                   'twitter_access_secret': getattr(c, 'twitter_access_secret', None),
                   'instagram_email': getattr(c, 'instagram_email', None),
                   'instagram_password': getattr(c, 'instagram_password', None),
                   'linkedin_access_token': getattr(c, 'linkedin_access_token', None),
                   'tumblr_access_token': getattr(c, 'tumblr_access_token', None),
                   'tumblr_access_secret': getattr(c, 'tumblr_access_secret', None),
                   }

    return credentials
