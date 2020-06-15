import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_question = questions[start:end]
  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # Reference from the Udacity lesson "flask-cors"
  #   CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories_all():

      try:
          categories = Category.query.all()

          # declare categories as dictionary
          categories_dict = {}
          # format category to match with front end react code
          for category in categories:
              categories_dict[category.id] = category.type

          # return response on successful
          return jsonify({
              'success': True,
              'categories': categories_dict,
              'status': 200
          })
          # abort with error code if there is exception
      except Exception:
          abort(500)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    questions =  Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.type).all()
    formatted_categories = {category.id: category.type for category in categories}
    current_questions = paginate(request, questions) 
    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'categories': formatted_categories,
      'total_questions': len(questions),
      'current_category': None
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      """Delete specific question

      This endpoint deletes a specific question by the
      id given as a url parameter
      """
      try:
          question = Question.query.get(id)
          question.delete()

          return jsonify({
              'success': True,
              'message': "Question successfully deleted",
              'status': 200
          })
      except Exception:
        return jsonify({
          'success': False,
          'status': 422
          })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_questions():
    question = request.get_json()
    # evaluate whether the data is not empty
    if question['question'] == '':
      error = "Not Complete"
      abort(500)
    try:
      Question(
        question=question['question'],
        answer=question['answer'],
        category=question['category'],
        difficulty=question['difficulty']
        ).insert()

      return jsonify({
        'question': question,
        'success': True,
        'message': 'Sucessfully posted questions',
        'status':200
        })

    except Exception:
      return jsonify({
        'success': False,
        'status': 422
        })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def filter_questions():
      """This endpoint returns questions from a search term. """

      # Get search term from request data
      data = request.get_json()
      search_term = data.get('searchTerm', '')
      # abort if search_term is empty with error code
      if search_term == '':
          abort(422)
      try:    
          search_data = Question.query.filter(Question.question.ilike(f'%{search_term}%'))  
          return jsonify({
            'success': True,
            'questions': [qn.format() for qn in search_data],
            'current_category': None
          })
      except Exception:
           abort(404)      
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_qns = [question.format() for question in questions]
    if len(formatted_qns) == 0:
      abort(404)
    return jsonify({
       'success': True,
      'questions': formatted_qns,
      'total_questions': len(formatted_qns),
      'current_category': category_id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quizzes():
    quiz_category = int(request.get_json()['quiz_category']['id'])
    previous_questions = request.get_json()['previous_questions']
    qn_list = [1,2,3,4,5,6]

    '''create random, and unique question for the category'''
    if quiz_category not in qn_list:
      unique_questions = Question.query.all()
    else:
      unique_questions = Question.query.filter_by(category=quiz_category).filter(Question.id.notin_(previous_questions)).all()

    if len(unique_questions) > 0:
      return jsonify({
        'success': True,
        'question': random.choice([qn.format() for qn in unique_questions]),
        'category_': quiz_category,
        'previous': [u.question for u in unique_questions]
      })
    else:
      return jsonify({
        'success': True,
        'question': None
      })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # Error handler for Not Found
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        "error": 404,
        "message": "Page Not Found"
      }), 404
  # Error handler for Unprocessed Entity
  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        "error": 422,
        "message": "Unprocessable entity"
      }), 422
  # Error handler for Internal Server Error
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        "error": 500,
        "message": "Internal Server error"
      }), 500    
  return app

    