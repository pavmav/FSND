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
  
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Constrol-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def categories():
    '''Endpoint to handle GET requests 
    for all available categories.
    '''
    
    try:

      categories = Category.query.all()

      categories_types = [c.type for c in categories]

      return jsonify({
        'categories': categories_types
      })

    except:
      print(sys.exc_info())
      abort(400)

  @app.route('/questions', methods=['GET'])
  def get_questions_paginated():
    '''Endpoint to handle GET requests for questions, 
    including pagination (every QUESTIONS_PER_PAGE questions). 
    This endpoint returns a list of questions, 
    number of total questions, current category and categories.
    '''

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


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    '''
    Endpoint to DELETE question using a question ID.
    '''

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


  @app.route('/questions', methods=['POST'])
  def create_search_question():
    '''Endpoint to POST a new question, 
    or search questions depending
    on the request body.
    '''

    print(request.get_json())

    try:
      question_data = request.get_json()

      question = question_data.get('question')
      answer = question_data.get('answer')
      difficulty = question_data.get('difficulty')
      category = question_data.get('category')
      search_term = question_data.get('searchTerm')

      if not search_term is None:
        
        questions = [q.format() for q in Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()]
        categories = Category.query.all()
        
        return jsonify({
          'questions': questions,
          'total_questions': len(questions),
          'categories': {category.id: category.type for category in categories},
          'current_category': None
        })

      else:

        if None in (question, answer, category, difficulty):
          abort(400)

        new_question = Question(question, answer, category, difficulty)

        new_question.insert()

        return jsonify({
          'success': True
        })

    except:
      print(sys.exc_info())
      abort(400)
      
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_in_category(category_id):
    '''Endpoint to get questions based on category.
    '''
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

  @app.route('/quizzes', methods=['POST'])
  def quiz():
    '''
    Endpoint to get questions to play the quiz. 
    This endpoint takes category and previous question parameters 
    and returns a random questions within the given category, 
    if provided, and that is not one of the previous questions.
    '''
   
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

    