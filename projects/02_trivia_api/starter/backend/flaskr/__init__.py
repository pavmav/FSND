import os
from flask import Flask, request, abort, jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from sqlalchemy.orm import query

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  V @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  '''
  V @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Constrol-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  V @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def categories():
    
    try:

      categories = Category.query.all()

      categories_types = [c.type for c in categories]

      return jsonify({
        'categories': categories_types
      })

    except:
      print(sys.exc_info())
      abort(400)

  '''
  V @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions_paginated():

    try:

      page = int(request.args['page'])

      start = (page - 1) * QUESTIONS_PER_PAGE
      end = (page * QUESTIONS_PER_PAGE)

      questions = [q.format() for q in Question.query.all()]
      categories = Category.query.all()
      
      return jsonify({
        'questions': questions[start:end],
        'total_questions': len(questions),
        'categories': {category.id: category.type for category in categories},
        'current_category': None
      })

    except:
      print(sys.exc_info())
      abort(400)


  '''
  V @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.get(question_id)

    if question is None:
      abort(404)

    try:

      question.delete()

      return jsonify({
        'success': True
      })

    except:
      print(sys.exc_info())
      abort(400)

  '''
  V @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():

    print(request.get_json())

    try:
      question_data = request.get_json()

      question = question_data.get('question')
      answer = question_data.get('answer')
      difficulty = question_data.get('difficulty')
      category = question_data.get('category')
      search_term = question_data.get('searchTerm')

      if search_term:
        
        questions = [q.format() for q in Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()]
        categories = Category.query.all()
        
        return jsonify({
          'questions': questions,
          'total_questions': len(questions),
          'categories': {category.id: category.type for category in categories},
          'current_category': None
        })

      else:

        new_question = Question(question, answer, category, difficulty)

        new_question.insert()

        return jsonify({
          'success': True
        })

    except:
      print(sys.exc_info())
      abort(400)
      
  '''
  V @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  

  '''
  V @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_in_category(category_id):
    try:

      questions = [q.format() for q in Question.query.filter(Question.category == category_id).all()]
      categories = Category.query.all()
      
      return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'categories': {category.id: category.type for category in categories},
        'current_category': None
      })

      return None
    except:
      print(sys.exc_info())
      abort(400)

  '''
  V @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    
    
    quiz_data = request.get_json()

    try:
      previous_questions = quiz_data['previous_questions']
      quiz_category = quiz_data['quiz_category']
      category_id = str(int(quiz_category['id']) + 1)
      any_category = quiz_category['type'] == 'click'
    except:
      print(sys.exc_info())
      abort(422)

    try:

      question_query = Question.query

      if not any_category:
        question_query = question_query.filter(Question.category == category_id)

      questions = question_query.filter(Question.id.notin_(previous_questions)).all()

      random_question = None

      if questions:
        random_question = random.choice(questions).format()

      return jsonify({
        'question': random_question
      })

    except:
      print(sys.exc_info())
      abort(400)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def something_went_wrong(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Request is unprocessable'
    }), 422

  return app

    