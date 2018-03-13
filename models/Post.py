import datetime

from blueprints.login.Login import load_user, get_current_user
from shared.models import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    image = db.Column(db.Text)
    social_network = db.Column(db.Text)
    date_posted = db.Column(db.DateTime(), default=datetime.datetime.now())
    link = db.Column(db.Text, default="#")
    user_email = db.Column(db.String(80), db.ForeignKey('users.email'))

    def __repr__(self):
        return '<Post:{} {} {} {} {} {} {}>' \
            .format(self.id, self.title, self.content, self.image,
                    self.social_network, self.user_email,
                    self.date_posted)


def insert_post_current_user(content, social_network, db, image="", title="", link="",
                             user=None):
    if user is None:
        user = load_user(get_current_user())

    import datetime
    time_indian = datetime.datetime.utcnow()
    time_indian = time_indian + datetime.timedelta(hours=5, minutes=30)

    post = Post(title=title, content=content, social_network=social_network, image=image,
                user=user, date_posted=time_indian, link=link)
    db.session.add(post)
    db.session.commit()
