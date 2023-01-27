from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Post, User, Neworder
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, VehicleForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


views = Blueprint('views', __name__)


@views.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.update_posted.desc()).paginate(page=page, per_page=5)
    neworders = Neworder.query.order_by(
        Neworder.order_posted_date.desc())

    return render_template('home.html', title='Home', posts=posts, neworders=neworders)


@views.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.update_posted.desc()).paginate(page=page, per_page=5)

    return render_template('user_post.html', title='User Posts', posts=posts, user=user)


@views.route('/user/order/<string:username>')
def user_order(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    userorder = Neworder.query.filter_by(author=user).order_by(
        Neworder.order_posted_date.desc()).paginate(page=page, per_page=5)

    return render_template('user_order.html', title='User Orders', userorder=userorder, user=user)


@views.route('/about', methods=['Get', 'POST'])
def about():
    colours = ["White", "Yellow", "Grey", "Red", "Blue", "Black", "Orange"]
    return render_template('about.html', title='About', colours=colours)


@views.route('/newlogin', methods=['GET', 'POST'])
def newlogin():
    if current_user. is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('newlogin.html', title='New Login', form=form)
