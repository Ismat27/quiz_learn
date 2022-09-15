from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from flask import jsonify, abort,  request
from sqlalchemy import or_
from .models import User, db
from .errors import error400, error404, error422, error_msg

def create_user():
    data = request.get_json()
    try:
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    except KeyError:
        return error_msg(message='missing data', code=400)
    for key in data.keys():
        if not data[key]: return error400()
    current_user = User.query\
                .filter(or_(User.email==email[0], User.username==username[0]))\
                .first()
    if current_user:
        return error_msg(message='email or username taken', code=409)
    try:
        user = User(
            public_id = str(uuid.uuid4()).replace('-', ''),
            username=username[0],
            first_name=first_name[0],
            last_name=last_name[0],
            email=email[0],
            password=generate_password_hash(password)
        )
        user.insert()
        return jsonify({
            'success': True,
            'user': user.format()
        })
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
        'data': users,
        'success': True
    })

def user(user_id):
    user = User.query.get(user_id)
    if not user: return error404()
    return jsonify(user.format())

def login_user():
    data = request.get_json()
    if not data:
        return error400('login details not provided')
    try:
        # email = data['email']
        username = data['username']
        password = data['password']
    except KeyError:
        return error400('missing data')
    for key in data.keys():
        if not data[key]: return error400()
    user = User.query.filter_by(username=username).first()
    if not user:
        return error404(message='user not found')
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

    return error422('incorrect credentials')