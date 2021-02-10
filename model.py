from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


class Cellist(db.Model):
    """Data model for a cellist."""

    __tablename__ = "cellists"

    cellist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    cello_details = db.Column(db.Text())
    bio = db.Column(db.Text)
    img_url = db.Column(db.Text)
    music_url = db.Column(db.Text)

    def __repr__(self):
        """Display info about Cellist."""

        return f'<Cellist cellist_id={self.cellist_id}, fname={self.fname}, lname={self.lname}>'

    # test_c = Cellist(fname='Cori', lname='Lint', location='Tulsa', cello_details='2014 Y. Chen, Cleveland OH', bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', img_url='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', music_url='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')


class Link(db.Model):
    """Data model for a teacher/student link."""

    __tablename__ = "links"

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_year = db.Column(db.DateTime)
    end_year = db.Column(db.DateTime)
    location = db.Column(db.String(50))

    def __repr__(self):
        """Display info about teacher/student link."""

        return f'<Link link_id={self.link_id} start_year={self.start_year}>'

    # link = Link(start_year='2014', end_year='2018', location='Cleveland')


class Post(db.Model):
    """Data model for forum post."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def __repr__(self):
        """Display info about forum post."""

        return f'<Post post_id={self.post_id}>'
        

class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Display info about User."""

        return f'<User user_id={self.user_id}, username={self.username}, email={self.email}>'

        # test_user = User(username='tester', email='test@test.com', password='123')

class Role(db.Model):
    """Data model for a user/admin role."""

    __tablename__ = "roles"

    role_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin = db.Column(db.Boolean)
    moderator = db.Column(db.Boolean)
    user = db.Column(db.Boolean)

    def __repr__(self):
        """Display info about Role."""

        return f'<Role role_id={self.role_id}, user={self.user}>'

        # tr = Role(admin='False', moderator='False', user='True')


def connect_to_db(flask_app, db_uri='postgresql:///test', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')        





if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

    