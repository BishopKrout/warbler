import os
import unittest
import signal
from datetime import datetime
from unittest import TestCase
from models import db, User, Message
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
db.create_all()

class MessageModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@example.com",
                                    password="testpassword",
                                    image_url=None)
        
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_message_creation(self):
        """Does creating a message work?"""
        msg = Message(text="Hello World", user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        # Check the message is in the database
        msgs = Message.query.all()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].text, "Hello World")


    def test_message_deletion(self):
        """Does deleting a message work?"""
        msg = Message(text="Goodbye World", user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        # Ensure the message was added
        self.assertEqual(len(Message.query.all()), 1)

        # Delete the message
        db.session.delete(msg)
        db.session.commit()

        # Check the message is no longer in the database
        self.assertEqual(len(Message.query.all()), 0)


    def test_message_likes(self):
        """Does liking a message work?"""
        msg1 = Message(text="I love coffee", user_id=self.testuser.id)
        msg2 = Message(text="I love beef", user_id=self.testuser.id)
        db.session.add_all([msg1, msg2])
        db.session.commit()

        self.testuser.likes.append(msg1)
        db.session.commit()

        # Check the likes
        likes = self.testuser.likes
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].id, msg1.id)
        pass

if __name__ == '__main__':
    unittest.main()
