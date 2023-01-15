"""
    routers.py
"""

from datetime import datetime
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from flask_paginate import Pagination
from .models import Post
from app import db


DATE_FORMAT = '%d %B %Y %H:%M'
PER_PAGE = 15

# Blueprint Configuration
main = Blueprint(
    'main', __name__,
    template_folder='templates'
)

@main.route('/', methods=['GET'])
# @main.route('/index', methods=['GET'])
def index():
    """ Index Page """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.\
        filter(Post.forward<2).\
        filter(Post.pub_date >= datetime.now().date()).\
        order_by(Post.pub_date.asc()).\
        paginate(page, PER_PAGE, False)

    pagination = Pagination(
        page=page,
        per_page=PER_PAGE,
        total=posts.total,
        record_name="posts",
        format_total=True,
        format_number=True,
    )

    return render_template('index.html', posts=posts.items,
                           pagination=pagination)

@main.route('/<int:post_id>')
def post(post_id):
    """ Show Post """
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post,
                           last_modified = post.last_modified.strftime(DATE_FORMAT))

@main.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """ Create new Post """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            new_post = Post(title=title, content=content, ovner=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template('create.html')

@main.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """ Edit Post """
    post = db.session.get(Post, id)

    if current_user.id <= post.ovner:

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            pub_date = request.form['pub_date']
            if 'forward' in request.form:
                forward  = True
            else:
                forward  = False

            if not title:
                flash('Title is required!')
            else:
                post.set_title(title)
                post.set_content(content)
                post.set_pub_date(pub_date)
                post.set_forward(forward)
                db.session.commit()
                return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.profile'))

    return render_template('edit.html', post=post)

@main.route('/<int:id>/delete', methods=('POST','GET'))
@login_required
def delete(id):
    """ Delete Post """
    post = Post.query.get_or_404(id)
    if current_user.id <= post.ovner:
        db.session.delete(post)
        db.session.commit()
        flash('"{}" was successfully deleted!'.format(post))
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    """ Show Profile curent User """
    return render_template('profile.html', user=current_user)
