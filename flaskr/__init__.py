from flask import Flask, jsonify, request
from flask_cors import CORS
from .auth import get_token
from .referrals import create_referral
from .dashboard import user_dashboard_detail
from .users import user, create_user, all_users, login_user, update_user
from .quiz import  get_quiz_questions, mark_quiz, quiz_sessions, delete_quiz_session
from .question import create_question, all_questions, question_data
from .leaderboard import leaderboard_data
from .payments import all_transactions, confirm_payment, initiate_payment
from .errors import resource_not_found, bad_request, not_allowed, not_authorized, not_processable,\
    resource_already_exist,access_denied
from config import DevelopmentConfig

from .models import setup_db
def create_app(test_config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(test_config)
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

    @app.route('/users/<user_id>/', methods=['PUT', 'PATCH'])
    @get_token
    def edit_user(current_user, user_id):
        return update_user(current_user.public_id)
    
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

    @app.route('/quiz-question/')
    @get_token
    def _quiz_question(current_user):
        return get_quiz_questions(current_user)
    
    @app.route('/mark-quiz/', methods=['POST'])
    @get_token
    def _mark_quiz(current_user):
        return mark_quiz(current_user=current_user)

    @app.route('/questions/', methods=['POST'])
    @get_token
    def new_question(current_user):
        return create_question()
    
    @app.route('/questions/')
    def read_all_questions():
        return all_questions()
    
    @app.route('/questions/<int:id>/')
    def _question(id):
        return question_data(id)

    @app.route('/quiz-sessions/')
    def _quiz_sessions():
        return  quiz_sessions()
    
    @app.route('/quiz-sessions/<int:session_id>/', methods=['DELETE'])
    def quiz_session(session_id):
        if request.method == 'DELETE':
            return delete_quiz_session(session_id=session_id)

    @app.route('/leaderboard/')
    def leaderboard():
        return leaderboard_data()

    @app.route('/confirm-payment/', methods=['POST'])
    @get_token
    def _confirm_payment(current_user):
        return confirm_payment(current_user)

    @app.route('/initiate-payment/', methods=['POST'])
    @get_token
    def _initiate_payment(current_user):
        return initiate_payment(current_user)

    @app.route('/transactions/')
    def _transactions():
        return all_transactions()

    return app
