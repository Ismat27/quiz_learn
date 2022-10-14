import os,  requests, pytz, uuid
from datetime import datetime
from dotenv import load_dotenv
from flask import jsonify, abort, request
from sqlalchemy import desc
from .models import Wallet, WalletTransaction

load_dotenv()
PAYSTACK_TEST_SECRET = os.environ.get('PAYSTACK_TEST_SECRET')
PAYSTACK_TEST_PUBLIC = os.environ.get('PAYSTACK_TEST_PUBLIC')

my_timezone = pytz.timezone('Africa/Lagos')
today = datetime.now(my_timezone)

def deposit():
    pass

def initiate_payment(current_user):
    try:
        request_data = request.get_json()
        email = request_data['email']
        if not email == current_user.email:
            abort(403, description="email not for user")
        return jsonify(PAYSTACK_TEST_PUBLIC)
    except Exception:
        abort(400, description="email not sent")

def confirm_payment(current_user):
    try:
        request_data = request.get_json()
        payment_reference = request_data['reference']
        transaction_type = request_data.get('transaction_type', 'deposit')
    except Exception:
        abort(400, description="reference not sent")

    user_wallet = Wallet.query.filter(
        Wallet.user==current_user
    ).first()

    if not user_wallet:
        user_wallet = Wallet(
            public_id = str(uuid.uuid4()).replace('-', ''),
            user_id=current_user.id,
            balance=0,
        )
        user_wallet.insert()
    
    url = 'https://api.paystack.co/transaction/verify/{}'.format(payment_reference)
    try:
        headers = {'Authorization': f'Bearer {PAYSTACK_TEST_SECRET}'}
        r = requests.get(url, headers=headers)
        resp = r.json()
        data = resp['data']
        success = data['status']
    except requests.exceptions.HTTPError:
        abort(422, description="payment verification not properly done")
    except IndexError:
        abort(422, description="index error")
    except Exception as error:
        print(error)
        abort(422, description="unable to verify payment")
    try:
        if success == 'success':
            status = data['status']
            amount = data['amount']
            transaction = WalletTransaction(
                public_id = str(uuid.uuid4()).replace('-', ''),
                wallet_id=user_wallet.id,
                amount=amount/100,
                status=status,
                transaction_type=transaction_type,
                timestamp=datetime.now(my_timezone),
                paystack_reference=payment_reference
            )
            transaction.insert()
            user_wallet.balance += amount
            return jsonify('success')
    except Exception as error:
        print(error)
        abort(422, description="unable to save payment")


def all_transactions():
    transactions = WalletTransaction.query.order_by(
        desc(WalletTransaction.timestamp)
    ).all()

    transactions = [
        transaction.format() for
        transaction in transactions
    ]

    return jsonify(transactions)

def user_transactions(current_user):
    transactions = WalletTransaction.query.filter(
        Wallet.user==current_user
    ).order_by(
        desc(WalletTransaction.timestamp)
    ).all()

    transactions = [
        transaction.format() for
        transaction in transactions
    ]

    return jsonify(transactions)

def delete_transaction():
    pass

def update_transaction():
    pass

def wallets():
    pass

def user_wallet():
    pass
