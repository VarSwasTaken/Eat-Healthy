from importlib.resources import path
from flask import render_template, flash, redirect, request, url_for, send_file
from jinja2 import Undefined
from app import app
from app.db import db
from app.forms import LoginForm, RegistrationForm, CreatePostForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from io import BytesIO

from app.models.user import User
from app.models.post import Post

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.article_published.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title="Home", posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/<author>/post', methods=['GET', 'POST'])
@login_required
def make_post(author):
    form = CreatePostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=author).first()
        post = Post(title=form.title.data, description=form.description.data, url=form.url.data, content=form.post.data, author=user)
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as error:
            flash('Something went wrong')
            return render_template('post.html', form=form)

        return redirect(post.url)

    return render_template('post.html', form=form)

@app.route('/<author>/<url>')
def posts(author, url):
    post = Post.query.filter_by(url=url).join(User).filter_by(username=author).first()

    return render_template('article.html', post=post)

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]

    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(User).filter_by(username=username).order_by(Post.article_published.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = username + '?page=' + str(posts.next_num) \
        if posts.has_next else None
    prev_url = username + '?page=' + str(posts.prev_num) \
        if posts.has_prev else None

    return render_template('profile.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/admin')
@login_required
def admin():
    print(current_user.admin)
    if not current_user.admin:
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.article_published.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('admin.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # photo = Undefined
        # with open(os.path.dirname('static/img/default_logo.png'), 'rb') as file:
        #     photo = file.read()
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # user.set_photo(url_for('static', filename='img/default_logo.png'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)
