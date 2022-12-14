from flask import jsonify
from sqlalchemy import desc
from .models import QuizSession
from .errors import error400, error422

def user_dashboard_detail(user):
    if not user:
        return error400()
    referrals = []

    sessions = []
    quizzes = QuizSession.query.filter(
        QuizSession.user_id==user.id
    ).order_by(desc(QuizSession.date_created)).all()
    if quizzes:
        sessions = [
            quiz.format() for quiz in quizzes
        ]
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
            'cap': user.cap,
            'cp': user.cp,
        })
    except Exception as error:
        print(error)
        return error422()
    
