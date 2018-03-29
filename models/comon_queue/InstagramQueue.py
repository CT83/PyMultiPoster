from shared.models import db


class InstagramQueue(db.Model):
    __bind_key__ = 'common_queue'
    id = db.Column(db.Integer, primary_key=True)
