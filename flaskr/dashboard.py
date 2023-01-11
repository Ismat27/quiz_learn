from flask import jsonify
from sqlalchemy import desc
from .models import QuizSession, Leaderboard
from .errors import error400, error422

def user_dashboard_detail(user):
    if not user:
        return error400()
    referrals = []

    sessions = []
    quizzes = QuizSession.query.filter(
        QuizSession.user_id==user.id
    ).order_by(
        desc(QuizSession.score), desc(QuizSession.last_updated)
    ).all()
    if quizzes:
        sessions = [
            quiz.format() for quiz in quizzes
        ]
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
    try:
        user_referrals = user.referrals
        if user_referrals:
            referrals = [
                referral.format() for
                referral in user_referrals
            ]
        return jsonify({
            'referrals': referrals,
            'total_referrals': len(referrals),
            'total_points': user.cap + user.cp,
            'quiz_sessions': sessions,
            'leaderboard': leaderboard,
            'cap': user.cap,
            'cp': user.cp,
        })
    except Exception as error:
        print(error)
        return error422()
    
