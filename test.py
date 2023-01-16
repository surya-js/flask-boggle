from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_display_board(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:

            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('no_plays'))
            
    def test_valid_word(self):
        """Test if the word is valid by modifying the board in the session"""

        with app.test_client() as client:

            with client.session_transaction() as session:
                session['board'] = [["H", "O", "P", "T", "A"], 
                                    ["H", "O", "P", "T", "A"], 
                                    ["H", "O", "P", "T", "A"], 
                                    ["H", "O", "P", "T", "A"], 
                                    ["H", "O", "P", "T", "A"]]

            response =client.get('/check-word?word=hop')
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the board"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=invalid')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_word(self):
        """Test if word is on the dictionary"""

        with app.test_client() as client:
            client.get('/')
            response =client.get(
                '/check-word?word=jhjfjhgjlh')
            self.assertEqual(response.json['result'], 'not-a-word')


