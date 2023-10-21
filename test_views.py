import unittest
from datetime import datetime
from app import app, db
from models import User, Message

class ViewsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler_test'  # Use a separate test database
        app.config['SERVER_NAME'] = 'localhost.localdomain'  # Set SERVER_NAME for request context
        app.config['TESTING'] = True  # Set TESTING flag for better error reporting
        db.create_all()  # Create tables for testing

    @classmethod
    def tearDownClass(cls):
        db.drop_all()  # Drop all tables after tests

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.test_request_context():
            user = User(email='testuser@example.com', username='testuser', password='password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        db.session.remove()  # Remove session
        self.app_context.pop()  # Pop app context

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_message_page(self):
        user = User.query.filter_by(username='testuser').first()
        message = Message(text='test message', user_id=user.id, timestamp=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        response = self.app.get('/messages')
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        response = self.app.get('/profile/testuser')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
