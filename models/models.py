# from flask_sqlalchemy import SQLAlchemy
#
# from app import app
#
# database = SQLAlchemy(app)
#
#
# class User(database.Model):
#     email = database.Column(database.String(80), primary_key=True, unique=True)
#     password = database.Column(database.String(80))
#
#     def __init__(self, email, password):
#         self.email = email
#         self.password = password
#
#     def __repr__(self):
#         return '<User %r>' % self.email
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return str(self.email)