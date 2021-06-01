from server import app
from model import db, connect_to_db
import unittest
import test_db

class serverTests(unittest.TestCase):
    """Runs tests on routes/page render"""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client() # test_client from Werkzeug library returns a "browser" to "run" app
        app.config['TESTING'] = True

    def test_homepage(self):
        """Does homepage load?"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1 class="text-center main-title">Cello<br>Tree</h1>', result.data)

    # TODO: user login


# class TestDb(unittest.TestCase):
#     """Runs tests on database"""

#     def setUp(self):
#         """Code to run before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         connect_to_db(app, db_uri='postgresql:///pt')

#         db.create_all()
#         test_db.test_all()
#         ####### ** see db_tests.py for test_all function ** #######

#     def test_homepage(self):
#         """Can I add everything to my db?"""

#         result = self.client.get('/')
#         self.assertEqual(result.status_code, 200)
#         self.assertIn(b'<h1 class="text-center main-title">Cello<br>Tree</h1>', result.data)

#     def tearDown(self):
#         """Code to run after every test"""

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()


if __name__ == "__main__":
    unittest.main(verbosity=2)