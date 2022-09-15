from flask import Flask, jsonify
from flask_cors import CORS
from .auth import get_token
from .referrals import create_referral
from .dashboard import user_dashboard_detail
from .users import user, create_user, all_users, login_user

from .models import setup_db
def create_app(test_config=None):
    app = Flask(__name__)
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
    
    return app
