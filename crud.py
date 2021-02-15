from model import db, connect_to_db, Cellist, Link, Post, Upvote, User

from datetime import datetime, timezone, timedelta

def create_cellist(fname, lname, cello_details, bio, img_url, music_url):
    """Create a cellist profile."""
    cellist = Cellist(fname=fname, lname=lname, cello_details=cello_details, bio=bio, img_url=img_url, music_url=music_url)

    db.session.add(cellist)
    db.session.commit()

    return cellist
# create_cellist('cori', 'lint', 'tulsa', 'woeiraoier', 'owierjwoi', 'keurhtihiugrh')

def get_cellist_by_id(cellist_id):
    """Returns cellist object given cellist id."""
    return Cellist.query.get(cellist_id)

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


def create_link():
    """Create a teacher/student link."""
    pass


def create_post(user_id, cellist_id, content, post_date):
    """Create a post on a cellist profile."""
    # use Post model to create a post 
    # get user id from session to assign user id
    post = Post(user_id=user_id, cellist_id=cellist_id, content=content, post_date=post_date)

    db.session.add(post)
    db.session.commit()

    return post

def edit_post():
    """Edit an existing post. Only the post creator, an admin, or moderator can do this."""
    pass


def delete_post():
    """Delete a post. Only the post creator, an admin, or moderator can do this."""
    pass


def upvote_post():
    """Upvote a post."""
    pass


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