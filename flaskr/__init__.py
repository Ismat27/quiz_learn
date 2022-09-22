from flask import Flask, jsonify
from flask_cors import CORS
from .auth import get_token
from .referrals import create_referral
from .dashboard import user_dashboard_detail
from .users import user, create_user, all_users, login_user
from .quiz import  quiz_question
from .question import create_question, all_questions, question_data
from .errors import resource_not_found, bad_request, not_allowed, not_authorized, not_processable,\
    resource_already_exist,access_denied

from .models import setup_db
def create_app(test_config=None):
    app = Flask(__name__)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, not_authorized)
    app.register_error_handler(403, access_denied)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405, not_allowed)
    app.register_error_handler(409, resource_already_exist)
    app.register_error_handler(422, not_processable)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def hello():
        return jsonify('You are welcome to QuizLearn')
    
    @app.route('/users/')
    def read_all_users():
        return all_users()

    @app.route('/users/<int:user_id>/')
    def read_user(user_id):
        return user(user_id)
    
    @app.route('/signup/', methods=['POST'])
    def signup():
        return create_user()

    @app.route('/login/', methods=['POST'])
    def login():
        return login_user()
    
    @app.route('/referrals/', methods=['POST'])
    def new_referral():
        return create_referral()
    
    @app.route('/dashboard/')
    @get_token
    def dashboard(current_user):
        return user_dashboard_detail(current_user)

    @app.route('/quiz-question/', methods=['POST'])
    def _quiz_question():
        return quiz_question()

    @app.route('/questions/', methods=['POST'])
    def new_question():
        return create_question()
    
    @app.route('/questions/')
    def read_all_questions():
        return all_questions()
    
    @app.route('/questions/<int:id>/')
    def _question(id):
        return question_data(id)

    return app
