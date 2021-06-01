from model import *
from crud import *

def test_all():
    test_user()
    # test_cellist()
    # test_link()
    # test_post()
    # test_upvote()

def test_user():
    """Creates test User in test database"""
    create_user('Guppy', 'guppy@thecat.com', 'badpw')


# def test_cellist():
#     """Creates test Cellist in test database"""
#     upload_image(
#         'https://s.keepmeme.com/files/en_posts/20200822/cc83fa3c7f8f8d04b3cdb12d65d57101confused-cat-with-a-lot-of-question-marks.jpg',
#         'this cat is CONFUSE',
#         1,
#         False,
#         None
#         )


# def test_link():
#     """Creates test Link in test database"""

#     test_link = Tag(
#         name='honey badgers', 
#         icon='fas fa-badger-honey',
#         hex_code='#FFC0CB',
#         user_id=1)
#     db.session.add(test_link)
#     db.session.commit()

# def test_post():
#     """Creates test Post in test database"""
#     pass

# def test_upvote():
#     """Creates test Upvote in test database"""
#     pass