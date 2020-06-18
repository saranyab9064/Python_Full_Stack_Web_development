import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('sara', 'sara','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Response status is not 200')
        self.assertEqual(data['success'], True)

    def test_questions_with_pagination(self):
        response = self.client().get('questions?page=1')    
        data = json.loads(response.data)
        self.assertEqual(len(data['questions']), 10, 'Result is not limited to 10 questions')  

    def test_questions_for_a_category(self):
        response = self.client().get('categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Response status is not 200') 
        self.assertTrue(data['questions'])  

    def test_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Response status is not 200')  

    def test_create_new_questions(self):
        data = {
            'question': 'What is the most beautiful park in the world?',
            'answer': 'Hyde Park, London',
            'category': 3,
            'difficulty': 1
        }
        response = self.client().post('/questions', json = data)
        self.assertEqual(response.status_code, 200, 'POST question is not succesful!') 

    def test_search_from_questions(self):
        body = {'searchTerm': 'Taj Mahal'}
        response = self.client().post('/search', json=body)
        data = json.loads(response.data)
        self.assertTrue((len(data['questions'])), '1')  

    def test_delete_the_post_questions(self):

        body = {'searchTerm': 'Taj Mahal'}
        response = self.client().post('/search', json=body)
        data = json.loads(response.data)
        self.assertTrue((len(data['questions'])), '1')  

    def test_quizzes(self):
        body= {
            'quiz_category':{
                'id': 2 
            },  
            'previous_questions': []
        }
        response = self.client().post('/quizzes', json=body)
        data = json.loads(response.data)
        self.assertEqual((data['category_']), 2, 'Category do not match')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
