from flask import render_template

from blog import app
from .database import session
from .models import Post
from flask import url_for
## added for login
from flask.ext.login import login_required

## added for author
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import *

@app.route("/")
@app.route("/page/<int:page>")
@login_required
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        #is_owner = False
        #current_user = current_user
    )  #isauth or is postowner.

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

import mistune
from flask import request, redirect, url_for

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

########## extend starts here ####################

@app.route("/post/<int:id>")
def one_post(id):
    post = session.query(Post).filter(Post.id == id).first() # sb first

    return render_template("onepost.html",
        post=post
    )


@app.route("/post/<int:id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    #########################################################################
    
    post = session.query(Post).filter(Post.id == id).first()
  
    print "post id is {}".format(post.id)
    print "post author is {}".format(post.author_id)
    print "current user id is {}".format(current_user.id)
    
    if post.author_id == current_user.id:
        return render_template("edit_post.html",post=post)  #could pass isowner here
    else:
        return render_template("security.html",message="Sorry you can't edit another user's post")

@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    
    if post.author_id == current_user.id:
        return render_template("edit_post.html",post=post)
    else:
        return abort(403)
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<int:id>/delete", methods =["GET"])
def delete_post_get(id):
    post = session.query(Post).get(id)
    if post is None:
        abort(404)
    else:
        if post.author_id == current_user.id:
            session.delete(post)
            session.commit()
            return redirect(url_for("posts"))
        else:
            abort(403)

### added for login
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

from flask import flash
from flask.ext.login import login_user
from flask.ext.login import logout_user  ## working here for logout
from werkzeug.security import check_password_hash
from .models import User

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))

# @app.route("/logout",methods=["GET"])
# def logout():
#         flask.ext.login.logout_user()
#         return redirect(url_for("posts"))

### modified version of logout from flask doc https://flask-login.readthedocs.org/en/latest/
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html")
    
