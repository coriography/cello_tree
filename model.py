from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


class Cellist(db.Model):
    """Data model for a cellist."""

    __tablename__ = "cellists"

    cellist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    cello_details = db.Column(db.Text())
    bio = db.Column(db.Text)
    img_url = db.Column(db.Text)
    music_url = db.Column(db.Text)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    link = db.Column(db.Integer, db.ForeignKey('links.link_id'))

    creator = db.relationship('User', foreign_keys=[creator_id], backref='cellist_profiles')
    # teacher_links: a list of Link objects associated with Cellist.
    # student_links: a list of Link objects associated with Cellist.

    def __repr__(self):
        """Display info about Cellist."""

        return f'<Cellist cellist_id={self.cellist_id}, fname={self.fname}, lname={self.lname}>'

    # test_c = Cellist(fname='Cori', lname='Lint', cello_details='2014 Y. Chen, Cleveland OH', bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', img_url='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', music_url='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')


class Link(db.Model):
    """Data model for a teacher/student link."""

    __tablename__ = "links"

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('cellists.cellist_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('cellists.cellist_id'), nullable=False)
    start_year = db.Column(db.DateTime)
    end_year = db.Column(db.DateTime)
    location = db.Column(db.String(50))

    teacher = db.relationship('Cellist', foreign_keys=[teacher_id], backref='teacher_links')
    student = db.relationship('Cellist', foreign_keys=[student_id], backref='student_links')

    def __repr__(self):
        """Display info about Link."""

        return f'<Link link_id={self.link_id} teacher_student_link={self.teacher} / {self.student}>'

    # link = Link(teacher_id='1', student_id='1')


class Location(db.Model):
    """Data model for a cellist location."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cellist_id = db.Column(db.Integer, db.ForeignKey('cellists.cellist_id'), nullable=False)
    loc_type = db.Column(db.String(50), nullable=False)

    cellist = db.relationship('Cellist', foreign_keys=[cellist_id], backref='locations')

    def __repr__(self):
        """Display info about Location."""

        return f'<Location location_id={self.location_id} cellist={self.cellist_id}>'


class Post(db.Model):
    """Data model for forum post."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    cellist_id = db.Column(db.Integer, db.ForeignKey('cellists.cellist_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)

    # upvotes: a list of Upvote objects associated with Post. 
    cellist = db.relationship('Cellist', backref='posts')
    user = db.relationship('User', backref='posts')

    def __repr__(self):
        """Display info about Post."""

        return f'<Post post_id={self.post_id} cellist_id={self.cellist_id}>'

        # post = Post()


class Upvote(db.Model):
    """Data model for post upvote."""

    __tablename__ = "upvotes"

    upvote_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    count = db.Column(db.Integer, nullable=False)

    post = db.relationship('Post', backref='upvotes')
    user = db.relationship('User', backref='upvotes')

    def __repr__(self):
        """Display info about Upvote."""

        return f'<Upvote upvote_id={self.upvote_id}, count={self.count}>'


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False) # or use Role table???

    # cellist_profiles: a list of Cellist objects associated with User.
    # posts: a list of Post objects associated with User.
    # upvotes: a list of Upvote objects associated with User.

    def __repr__(self):
        """Display info about User."""

        return f'<User user_id={self.user_id}, username={self.username}, email={self.email}>'

        # test_user = User(username='tester', email='test@test.com', password='123')

# class Role(db.Model):
#     """Data model for a user/admin role."""

#     __tablename__ = "roles"

#     role_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     r_admin = db.Column(db.Boolean)
#     r_moderator = db.Column(db.Boolean)
#     r_user = db.Column(db.Boolean)
#       # or: role = db.Column(db.String(50)) #admin, moderator, or user
#       # user = db.relationship('User', backref='role')

#     def __repr__(self):
#         """Display info about Role."""

#         return f'<Role role_id={self.role_id}, user_id={self.user_id}>'

#         # tr = Role(admin='False', moderator='False', user='True')


def connect_to_db(flask_app, db_uri='postgresql:///tree', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')        



if __name__ == '__main__':
    print("we're in model")
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

    