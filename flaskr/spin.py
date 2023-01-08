from flask import jsonify, request, abort
from .models import Spin
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

    except Exception:
        abort(400)
