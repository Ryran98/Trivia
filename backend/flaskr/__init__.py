import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = page * QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in questions]

  return formatted_questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: (DONE) Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: (DONE) Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO (DONE): 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories = Category.query.all()
      category_dict = {}
      for category in categories:
        category_dict[category.id] = category.type

      return jsonify({
        'success': True,
        'categories': category_dict
      })

    except:
      abort(422)

  '''
  @TODO (DONE): 
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
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    selected_questions = paginate_questions(request, questions)

    categories = Category.query.all()
    category_dict = {}
    for category in categories:
      category_dict[category.id] = category.type

    if (len(selected_questions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'questions': selected_questions,
      'total_questions': len(questions),
      'categories': category_dict,
      'current_category': None
    })

  '''
  @TODO (DONE): 
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
        'success': True,
        'id': question.id
      })

    except:
      abort(422)
  '''
  @TODO (DONE): 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  @TODO (DONE): 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start.   
  '''
  @app.route('/questions', methods=['POST'])
  def create_or_search_questions():
    body = request.get_json()

    question_text = body.get('question', None)
    answer_text = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    searchTerm = body.get('searchTerm', None)

    if searchTerm:
      questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).order_by(Question.id)
      selected_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'questions': selected_questions,
        'total_questions': len(Question.query.all()),
        'current_category': None
      })
    else:
      if question_text is None or answer_text is None or difficulty is None or category is None:
        abort(422)
      
      try:
        question = Question(question=question_text, answer=answer_text, category=category, difficulty=difficulty)
        question.insert()

        return jsonify({
          'success': True,
          'id': question.id
        })

      except:
        abort(422)
  '''
  
  @TODO (DONE): 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
      abort(404)

    questions = Question.query.filter(Question.category == str(category.id))
    selected_questions = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': selected_questions,
      'total_questions': len(Question.query.all()),
      'current_category': category.type
    })

  '''
  @TODO (DONE): 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()

    category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)

    if category['id'] == 0:
      available_questions = Question.query.filter(Question.id.notin_(previous_questions))
    else:
      available_questions = Question.query.filter(Question.category == str(category['id']), Question.id.notin_(previous_questions))

    formatted_questions = [question.format() for question in available_questions]
    if len(formatted_questions) == 0:
      return jsonify({
        'success': True,
        'question': None
      })

    next_question = available_questions[random.randint(0, len(formatted_questions) - 1)].format()

    return jsonify({
      'success': True,
      'question': next_question
    })
  '''
  @TODO (DONE): 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  
  return app

    