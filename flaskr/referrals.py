import uuid
from flask import request, jsonify
from .models import Referral
from .errors import error400, error422

def create_referral():
    data = request.get_json()
    try:
        referral = Referral(
            public_id=str(uuid.uuid4()).replace('-', ''),
            commission=data['commission'],
            user_id=data['user_id'],
            refered_user_id=data['refered_user_id']
        )
        referral.insert()
        return jsonify({
            'success': True
        })
    except KeyError:
        return error400()
    except Exception as error:
        print(error)
        return error422

