import datetime

from shared.models import db


class InstagramQueuer(db.Model):
    __bind_key__ = 'common_queue'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    image_url = db.Column(db.Text, nullable=False)
    date_queued = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_email = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, default='queue')
