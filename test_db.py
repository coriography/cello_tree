from crud import *


def test_all():
    create_test_user()
    create_test_cellist()
    create_test_link()
    create_test_post()
    create_test_upvote()


def create_test_user():
    """Creates test User in test database"""
    test_user = create_user('Guppy', 'guppy@thecat.com', get_hash('badpw'))
    db.session.add(test_user)
    db.session.commit()


def create_test_cellist():
    """Creates test Cellist in test database"""
    test_cellist = create_cellist('Guppy', 'The Cat', 'Guppy plays a teeny tiny cello made in 2018 in Tulsa, OK',
                                  'Guppy started playing cello at the young age of 6 weeks. She became a virtuoso and made her debut at Carnegie Hall in 2019.',
                                  img_url="", music_url="guppythecat.com")
    db.session.add(test_cellist)
    db.session.commit()

    # TODO: add test for img_url on the front end


def create_test_link():
    """Adds second cellist and creates Link between first and second."""

    test_cellist_2 = create_cellist('Loja', 'The Cat', 'Loja plays a teeny tiny cello made in 2018 in Tulsa, OK',
                                    'Loja started playing cello at the young age of 6 weeks. She became a virtuoso and made her debut at Carnegie Hall in 2019.',
                                    img_url="", music_url='lojathecat.com')

    db.session.add(test_cellist_2)
    db.session.commit()

    test_link = create_link(1, 2)
    db.session.add(test_link)
    db.session.commit()


def create_test_post():
    """Creates test Post in test database"""
    test_post = create_post(1, 2, "omg best cellist everrrr", post_date=datetime.now(timezone.utc))
    db.session.add(test_post)
    db.session.commit()


def create_test_upvote():
    """Creates test Upvote in test database"""
    test_upvote = create_upvote(1, 1)
    db.session.add(test_upvote)
    db.session.commit()
