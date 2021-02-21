from model import db, connect_to_db, Cellist, Link, Post, Upvote, User

from datetime import datetime, timezone, timedelta

from flask_sqlalchemy import SQLAlchemy

def create_cellist(fname, lname, cello_details, bio, img_url="", music_url=""):
    """Create a cellist profile."""
    cellist = Cellist(fname=fname, lname=lname, cello_details=cello_details, bio=bio, img_url=img_url, music_url=music_url)

    db.session.add(cellist)
    db.session.commit()

    return cellist


def get_cellist_by_id(cellist_id):
    """Returns cellist object given cellist id."""
    return Cellist.query.get(cellist_id)


def get_cellist_by_name(fname, lname):
    """Returns cellist object given cellist name."""
    return Cellist.query.filter(Cellist.fname == fname, Cellist.lname == lname).first()


def get_all_cellists():
    """Get all cellists from database."""
    cellists = Cellist.query.order_by('lname').all()
    return cellists


def edit_cellist():
    """Edit a cellist profile."""
    pass


def update_owner():
    """Add or update owner of cellist profile."""
    pass


def create_link(teacher_id, student_id):
    """Create a teacher/student link."""

    link = Link(teacher_id=teacher_id, student_id=student_id)
    
    db.session.add(link)
    db.session.commit()

    return link


def check_link(teacher_id, student_id):
    """Return database row that matches given link."""

    return Link.query.filter(Link.teacher_id == teacher_id, Link.student_id == student_id).first()


def create_post(user_id, cellist_id, content, post_date):
    """Create a post on a cellist profile."""
    # use Post model to create a post 
    # get user id from session to assign user id
    post = Post(user_id=user_id, cellist_id=cellist_id, content=content, post_date=post_date)

    db.session.add(post)
    db.session.commit()

    return post


def get_posts_by_cellist(cellist_id):
    """Get all posts associated with Cellist and sort by date."""

    posts = Post.query.filter(Post.cellist_id == cellist_id).order_by(Post.post_date.desc()).all()

    return posts


def edit_post():
    """Edit an existing post. Only the post creator, an admin, or moderator can do this."""
    pass


def delete_post():
    """Delete a post. Only the post creator, an admin, or moderator can do this."""
    pass


def create_upvote(user_id, post_id):
    """Create an upvote on a post."""
    
    upvote = Upvote(user_id=user_id, post_id=post_id)
    db.session.add(upvote)
    db.session.commit()

    return upvote


def get_upvotes_count(post_id):
    """Get the count of upvotes for a given post."""

    count_upvotes = Upvote.query.filter(Upvote.post_id == post_id).count()

    return count_upvotes


def delete_upvote():
    """Delete an upvote. Only the upvote creator can do this."""
    pass


def create_user(username, email, password, role="user"):
    """Create a user."""
    user = User(username=username, email=email, password=password, role=role)

    db.session.add(user)
    db.session.commit()

    return user


def check_username(username):
    """Return database row that matches given username."""

    return User.query.filter(User.username == username).first()


def check_email(email):
    """Return database row that matches given email."""

    return User.query.filter(User.email == email).first()


def edit_user():
    """Update a user."""
    pass


def delete_user():
    """Delete a user."""
    pass


def update_role():
    """Update a user's role."""
    pass


if __name__ == '__main__':
    print("we're in crud")
    from server import app
    connect_to_db(app)