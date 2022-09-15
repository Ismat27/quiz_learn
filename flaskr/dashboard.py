from flask import jsonify
from .models import User
from .errors import error400, error422

def user_dashboard_detail(user):
    if not user:
        return error400()
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
        print(error)
        return error422()
    
