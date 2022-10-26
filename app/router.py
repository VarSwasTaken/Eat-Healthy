from flask import render_template, redirect, url_for, request, flash
from flask import render_template
from app import app
from app.forms import CreatePostForm
from app.models.post import Post
from app.db import db

from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models.user import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/<author>/post', methods=['GET', 'POST'])
@login_required
def make_post(author):
    form = CreatePostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=author).first()
        post = Post(post=form.title.data, url=form.url.data, content=form.post.data, author=user)
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

@app.route('/<author>')
def autor_posts(author):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(User).filter_by(username=author).order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = author + '?page=' + str(posts.next_num) \
        if posts.has_next else None
    prev_url = author + '?page=' + str(posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/admin')
@login_required
def admin():
    print(current_user.admin)
    if not current_user.admin:
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('admin.html', posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(current_user.username + '/post')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = current_user.username + '/post'
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)