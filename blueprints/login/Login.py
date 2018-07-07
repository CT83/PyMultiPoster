from functools import wraps

from flask import Blueprint, request, render_template, redirect, url_for, make_response
from flask_login import login_user, login_required, logout_user, current_user

from Forms.LoginForm import LoginForm
from Forms.SignupForm import SignupForm
from models.Users import Users
from shared.models import db, login_manager
from utils.SessionUtils import clear_session

login_blueprint = Blueprint('Login', __name__)


@login_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Users.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = Users(form.email.data, form.password.data, form.name.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return redirect(url_for('Login.login'))
        else:
            return "Form didn't validate"


@login_manager.user_loader
def load_user(email):
    return Users.query.filter_by(email=email).first()


def get_current_user():
    from flask_login import current_user
    if current_user.is_authenticated():
        return current_user.email
    else:
        return None


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    return "Wrong password!"
            else:
                return "user doesn't exist!"
    else:
        return "form not validated"


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    clear_session()
    resp = make_response(redirect(url_for('redirect_root')))
    return resp


def admin_login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view():
            print("Current User :", current_user.email, " Role :", current_user.role)
            if current_user.is_admin():
                return fn()
            else:
                return login_manager.unauthorized()

        return decorated_view

    return wrapper
