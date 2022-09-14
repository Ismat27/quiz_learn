from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from flask import jsonify, abort,  request
from sqlalchemy import or_
from flaskr.models import User, db

def create_user():
    data = request.get_json()
    if not data: abort(422)
    try:
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    except KeyError:
        return jsonify({
            'success': False,
            'message': 'missing data'
        }), 422
    for key in data.keys():
        print(f'{key} {data[key]}')
    # current_user = User.query\
    #             .filter(or_(User.email==email, User.username==username))\
    #             .first()
    # if current_user:
    #     abort(422, description='user already exist')
    try:
        user = User(
            public_id=str(uuid.uuid4()),
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password)
        )
        user.insert()
        return jsonify(user.format())
    except Exception as error:
        print(error)
        db.session.close()
        return jsonify({
            'success': False
        }), 422

def all_users():
    users = []
    db_users = User.query.all()
    if db_users:
        users = [
            user.format()
            for user in db_users
        ]
    return jsonify({
        'data': users
    })

def user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user not found',
            'success': False
        }), 404
    return jsonify(user.format())

def login_in_user():
    data = request.get_json()
    if not data:
        return jsonify({
            "message": "user details not provided",
            "error": "Bad request",
            'success': False
        }), 400
    
    try:
        email = data['email']
        password = data['password']
    except KeyError:
        return jsonify({
            'message': 'missing data',
            'success': False
        }), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            'message': 'incorrect credentials',
            'success': False
        }), 404
    if check_password_hash(user.password, password):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=7),
            }, 'thisisthesecretkey', algorithm='HS256'
        )
        return jsonify({
            'success': True,
            'token': token,
            'user': user.format()
        }), 200

    return jsonify({
        'message': 'incorrect credentials',
        'success': False
    }), 422