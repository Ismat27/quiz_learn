from flask import request, jsonify
from .models import Referral
def create_referral():
    data = request.get_json()
    try:
        referral = Referral(
            public_id=data['public_id'],
            commission=data['commission'],
            user_id=data['user_id'],
            refered_user_id=data['refered_user_id']
        )
        referral.insert()
        return jsonify({
            'success': True
        })
    except Exception as error:
        print(error)
        return jsonify({
            'success': False
        })
