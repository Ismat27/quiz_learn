from flask import jsonify
from .models import User

def user_dashboard_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user not found',
            'success': False
        }), 400
    referrals = []
    try:
        user_referrals = user.referrals
        if user_referrals:
            referrals = [
                referral.format() for
                referral in user_referrals
            ]
        return jsonify({
            'referrals': referrals
        })
    except Exception as error:
        return jsonify({
            'success': False
        })
