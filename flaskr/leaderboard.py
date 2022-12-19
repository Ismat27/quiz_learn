from flaskr.models import Leaderboard


from flask import jsonify
from sqlalchemy import desc
from .models import Leaderboard

def leaderboard_data():
    leaderboard = []
    board_data = Leaderboard.query.order_by(
        desc(Leaderboard.last_updated),
        desc(Leaderboard.points),
    ).all()
    if board_data:
        leaderboard = [
            data.format() for
            data in board_data
        ]
        leaderboard = sorted(
            leaderboard, key=lambda x: x["total_points"], reverse=True
        )
    return jsonify(leaderboard)
