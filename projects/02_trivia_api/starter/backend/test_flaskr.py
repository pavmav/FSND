import os
from re import search
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'trivia_test')

database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
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
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_categories_405_method_not_allowed(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['categories'])

    def test_questions_400_bad_request(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        res = self.client().delete('/questions/21')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Question.query.get(21), None)

        # restore question
        question = 'Who discovered penicillin?'
        answer = 'Alexander Fleming'
        category = 3
        difficulty = 1
        restore_question = Question(question, answer, category, difficulty)
        restore_question.id = 21

        restore_question.insert()

    def test_404_not_found_delete_question(self):
        res = self.client().delete('/questions/1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question(self):
        new_question_json = {
            'question': 'Foo?',
            'answer': 'Bar!',
            'category': 1,
            'difficulty': 5
        }

        res = self.client().post('/questions', json=new_question_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question_id'])

        new_question = Question.query.get(data['question_id'])
        self.assertFalse(new_question == None)

        # Delete new question
        new_question.delete()

    def test_create_question_400_bad_request(self):
        new_question_json = {
            'question': 'Foo?',
            'answer': 'Bar!',
            'category': 1
        }

        res = self.client().post('/questions', json=new_question_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_question(self):
        search_json = {'searchTerm': 'TiTlE'}

        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_get_questions_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 2)

    def test_get_questions_in_category_404(self):
        res = self.client().get('/categories/66/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_quiz(self):
        quiz_json = {
            'previous_questions': [20],
            'quiz_category': {
                'type': 'Science',
                'id': 0
            }
        }

        res = self.client().post('/quizzes', json=quiz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['id'], 22)

    def test_quiz_422_unprocessable(self):
        quiz_json = {
            'previous_questions': [20],
            'quiz_category': {
                'id': 0
            }
        }

        res = self.client().post('/quizzes', json=quiz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()