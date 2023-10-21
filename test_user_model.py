import os
from unittest import TestCase
from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        
        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@example.com",
                                    password="testpassword",
                                    image_url=None)
        
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_signup(self):
        """Does User.signup successfully create a new user?"""

        u_test = User.signup(username="testuser2",
                             email="test2@example.com",
                             password="testpassword",
                             image_url=None)
        db.session.commit()

        u = User.query.filter(User.username == "testuser2").first()
        self.assertIsNotNone(u)
        self.assertEqual(u.email, "test2@example.com")
        self.assertNotEqual(u.password, "testpassword")

    def test_user_authentication(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        user = User.authenticate(self.testuser.username, "testpassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.testuser.id)

    def test_invalid_username(self):
        """Does User.  authenticate fail to return a user when the username is invalid?"""

        self.assertFalse(User.authenticate("badusername", "testpassword"))

def test_wrong_password(self):
    """Does User.authenticate fail to return a user when the password is invalid?"""

    self.assertFalse(User.authenticate(self.testuser.username, "badpassword"))

if __name__ == "__main__":
    import unittest
    unittest.main()
