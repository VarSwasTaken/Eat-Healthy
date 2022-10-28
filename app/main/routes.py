
from flask import render_template, flash, redirect, request, url_for
from app.main import bp
from app.db import db
from app.main.forms import CreatePostForm
from flask_login import current_user, login_required

from app.models.user import User
from app.models.post import Post


@bp.route('/')
# @app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.article_published.desc()).paginate(
        page=page, per_page=bp.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title="Home", posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data,
                    url=form.url.data, content=form.content.data, author=current_user)
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash('Something went wrong')
            return render_template('post.html', form=form)

        return redirect(url_for('main.article', author=current_user.username, url=post.url))

    return render_template('post.html', form=form)


@bp.route('/<author>/<url>')
def article(author, url):
    post = Post.query.filter_by(url=url).join(
        User).filter_by(username=author).first()

    return render_template('article.html', post=post)


@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]

    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(User).filter_by(username=username).order_by(Post.article_published.desc()).paginate(
        page=page, per_page=bp.config['POSTS_PER_PAGE'], error_out=False)

    next_url = username + '?page=' + str(posts.next_num) \
        if posts.has_next else None
    prev_url = username + '?page=' + str(posts.prev_num) \
        if posts.has_prev else None

    return render_template('profile.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/<author>/<url>/edit', methods=['GET', 'POST'])
@login_required
def edit(author, url):
    if author != current_user.username and not current_user.admin:
        return redirect(url_for('mian.index'))

    form = CreatePostForm()
    post = Post.query.filter_by(url=url).join(
        User).filter_by(username=author).first()
    if request.method == 'GET':
        form.content.data = post.content_html

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.url = form.url.data
        post.content = form.content.data
        post.published = False
        db.session.commit()

        if current_user.admin:
            return redirect(url_for('main.admin'))
        return redirect(url_for('main.article', author=current_user.username, url=post.url))
    return render_template('post.html', form=form, post=post)


@bp.route('/<author>/<url>/publish')
@login_required
def publish(author, url):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    post = Post.query.filter_by(url=url).join(
        User).filter_by(username=author).first()
    print(post.published)
    post.published = True
    db.session.commit()

    return redirect(url_for('main.admin'))


@bp.route('/admin')
@login_required
def admin():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.article_published.desc()).paginate(
        page=page, per_page=bp.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.admin', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.admin', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('admin.html', posts=posts.items, next_url=next_url, prev_url=prev_url)