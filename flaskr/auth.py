from flask import request, jsonify, abort
from .models import User
import jwt
from functools import wraps

def get_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            abort(401)
        try:
            data = jwt.decode(token, 'thisisthesecretkey', algorithms=['HS256'])
            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except Exception as error:
            print(error)
            abort(401)
        return f(current_user, *args, **kwargs)
    return decorated