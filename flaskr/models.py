import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

db = SQLAlchemy()
migrate = Migrate()

def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    username = Column(String(200), server_default='unknown')
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(200))
    password = Column(Text)
    is_admin = Column(Boolean, server_default='f')
    is_superuser = Column(Boolean, server_default='f')
    signup_date = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now())
    cp = Column(Integer, nullable=False, default=0, server_default='0') # challenge points
    cap = Column(Integer, nullable=False, default=0, server_default='0') # course access points

    def __init__(self, **kwargs):
        self.public_id = kwargs['public_id']
        self.username = kwargs['username']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.email = kwargs['email']
        self.password = kwargs['password']

    def __repr__(self):
        return f'<User id: {self.id} name: {self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def fullname(self):
        if not self.first_name and not self.last_name:
            return self.username
        return f'{self.first_name} {self.last_name}'
    
    def format(self):
        return {
            'id': self.public_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'challenge_points': self.cp,
            'course_access_points': self.cap
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Referral(db.Model):
    __tablename__ = 'referrals'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    commission = Column(Numeric(10, 2))
    status = Column(Boolean, server_default='f')
    date_created = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='referrals', foreign_keys=[user_id])
    refered_user_id = Column(Integer, ForeignKey('users.id'))
    refered_user = relationship('User', backref=backref("refered_in", uselist=False), foreign_keys=[refered_user_id])
    

    def format(self):
        return {
            'commission': self.commission,
            'referred_user': self.refered_user.fullname(),
            'status': self.status,
            'date_created': self.date_created
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    name = Column(String(200), nullable=False)
    access_points = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Question(db.Model):
    """Table for quiz questions
        cp: challenge points
        cap: course access points
    """
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    cp_wrong = Column(Integer, nullable=False)
    cp_right = Column(Integer, nullable=False)
    cap_wrong = Column(Integer, nullable=False)
    cap_right = Column(Integer, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def quiz_format(self):
        options = [
            self.option_a, self.option_b,
            self.option_c, self.option_d,
        ]
        return {
            'options': options,
            'question': self.text,
            'id': self.id,
        }
    
    def format(self):
        options = [
            self.option_a, self.option_b,
            self.option_c, self.option_d,
        ]
        opt = ['a', 'b', 'c', 'd']
        correct_option = ''
        for (key, value) in zip(opt, options):
            if value == self.answer:
                correct_option = key
                break
        return {
            'options': options,
            'question': self.text,
            'correct_option': correct_option,
            'id': self.id,
            'date_created': self.date_created
        }

# class CoursePurchase(db.Model):
#     pass

# class Withdrawal(db.Model):
#     pass

# class EnrolledCourse(db.Model):
#     pass

class QuizSession(db.Model):
    """Table for quiz sessions users have taken
    """
    __tablename__ = 'quiz_sessions'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='quiz_taken', foreign_keys=[user_id])
    questions = Column(Text)
    score = Column(Integer, server_default='0')
    completed = Column(Boolean, server_default='f')
    date_created = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now())

    def __str__(self):
        return f'QuizSession taken by {self.user}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'taken_by': self.user.fullname(),
            'date': self.date_created,
            'score': self.score,
            'id': self.id,
            'completed': self.completed
        }

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref("leaderboard_profile", uselist=False), foreign_keys=[user_id])
    date_created = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now())
    cap = Column(Integer, nullable=False)
    cp = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.user.fullname(),
            'course_access_points': self.cap,
            'challenge_points': self.cp,
            'total_points': self.cp + self.cap,
            'score': self.points
        }

class Wallet(db.Model):

    __tablename__ = "user_wallets"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref("wallet", uselist=False), foreign_keys=[user_id])
    balance = Column(Numeric, nullable=False, default=0, server_default='0')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class WalletTransaction(db.Model):
    __tablename__ = "user_transactions"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(200), nullable=False)
    wallet_id = Column(Integer, ForeignKey('user_wallets.id'))
    wallet = relationship('Wallet', backref='transactions', foreign_keys=[wallet_id])
    amount = Column(Numeric, nullable=False)
    transaction_type = Column(String(50), default='subscription', server_default='subscription', nullable=False)
    status = Column(String(50), server_default='pending', nullable=False)
    paystack_reference = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    def __str__(self):
        return f'Made by {self.wallet.user.fullname()}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'user': self.wallet.user.fullname(),
            'timestamp': self.timestamp,
            'paystack_reference': self.paystack_reference,
            'amount': self.amount,
            'status': self.status,
            'type': self.transaction_type
        }