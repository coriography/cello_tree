from model import *
from crud import *

def test_all():
    test_user()
    test_cellist()
    # test_link()
    # test_post()
    # test_upvote()

def test_user():
    """Creates test User in test database"""
    create_user('Guppy', 'guppy@thecat.com', 'badpw')


def test_cellist():
    """Creates test Cellist in test database"""
    create_cellist('Guppy', 'The Cat', 'Guppy plays a teeny tiny cello made in 2018 in Tulsa, OK', 'Guppy started playing cello at the young age of 6 weeks. She became a virtuoso and made her debut at Carnegie Hall in 2019.', img_url="", music_url="")


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