from model import db, connect_to_db, Cellist, Link, Post, Upvote, User

def create_cellist():
    pass

def create_link():
    pass

def create_post():
    pass

def upvote_post():
    pass

def create_user():
    pass


if __name__ == '__main__':
    print("we're in crud")
    from server import app
    connect_to_db(app)