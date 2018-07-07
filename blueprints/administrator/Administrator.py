from flask import Blueprint, request, render_template
from flask_login import login_user, login_required

from Forms.SignupForm import SignupForm
from blueprints.login.Login import admin_login_required
from models.Post import Post
from models.Users import Users
from models.comon_queue.InstagramQueuer import InstagramQueuer
from shared.models import db
from table.models import UsersTable, PostTable

admin_blueprint = Blueprint('Administrator', __name__)


@admin_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    return "Form didn't validate"


@admin_blueprint.route('/admin_signup', methods=('GET', 'POST'))
@login_required
@admin_login_required()
def admin_signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('admin/admin_signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Users.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = Users(form.email.data, form.password.data, form.name.data, role=10)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return "Signed Up successfully as Admin"
        else:
            return "Form didn't validate"


@admin_blueprint.route('/admin_view')
@login_required
@admin_login_required()
def admin_view():
    return render_template('admin/admin_panel.html')


@admin_blueprint.route('/admin_view_users')
@login_required
@admin_login_required()
def admin_view_users():
    users = Users.query.all()
    InstagramQueuer.query.all()

    for user in users:
        user.link = user.email
        user.no = users.index(user) + 1
        user.no_of_posts = Post.query.filter_by(user_email=user.email).count()

    table = UsersTable(users)
    return render_template('admin/view_users.html', table=table)


@admin_blueprint.route('/admin_user_posts')
@login_required
@admin_login_required()
def admin_user_posts():
    user = request.args.get('username')
    posts = Post.query.filter_by(user_email=user).all()
    posts.reverse()  # Reverse Order of Posts
    for post in posts:
        post.no = posts.index(post) + 1
    table = PostTable(posts)
    return render_template('post/user_posts.html', table=table)
