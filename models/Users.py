from shared.models import db


class Users(db.Model):
    email = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))
    name = db.Column(db.Text)
    role = db.Column(db.Integer, default=1)  # Admin is level 10
    articles = db.relationship('Post', backref='user')

    def __init__(self, email, password, name, role=1):
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User {} {} {} {} {}>'.format(self.email, self.password, self.name, self.articles,
                                              self.role)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    def promote_to_admin(self):
        self.role = 10

    def is_admin(self):
        if self.role is not None:
            return self.role >= 10
        else:
            return False
