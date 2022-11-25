from flask import request, abort
import jwt
from functools import wraps

from .models import User
from .errors import error400, error401

def get_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return error401()
        try:
            data = jwt.decode(token, 'thisisthesecretkey', algorithms=['HS256'])
            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except jwt.ExpiredSignatureError:
            abort(403, description='session expired, login again')
        except Exception:
            return error400()
        return f(current_user, *args, **kwargs)
    return decorated