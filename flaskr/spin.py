import uuid
from flask import jsonify, request, abort
from .models import Spin, User
from .quiz import today


def all_spins():
    query = Spin.query.all()
    items = [
        item.format() for
        item in query
    ]
    return jsonify(items)

def new_spin():
    try:
        data = request.get_json()
        username = data['username']
        point = data['point']
    except Exception:
        abort(400)
    user = User.query.filter(
        User.username==username
    ).first()
    if not user:
        abort(404, description='unknown user')
    try:
        item = Spin(
            public_id = str(uuid.uuid4()).replace('-', ''),
            date_created=today,
            user_id=user.id,
            point=point,
        )
        item.insert()
    except Exception:
        abort(422)
    return jsonify(item.format())
