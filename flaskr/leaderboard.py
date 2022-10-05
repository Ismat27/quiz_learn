from flaskr.models import Leaderboard


from flask import jsonify
from sqlalchemy import desc
from .models import Leaderboard

def leaderboard_data():
    board_data = Leaderboard.query.order_by(
        desc(Leaderboard.points)
    ).all()
    board_data = [
        data.format() for
        data in board_data
    ]
    return jsonify(board_data)
