import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy()
migrate = Migrate()

def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
        return f'{self.first_name} {self.last_name}'
    
    def format(self):
        return {
            'id': self.public_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='referrals', foreign_keys=[user_id])
    refered_user_id = Column(Integer, ForeignKey('users.id'))
    refered_user = relationship('User', backref=backref("refered_in", uselist=False), foreign_keys=[refered_user_id])
    

    def format(self):
        return {
            'commission': self.commission,
            'referred_user': self.refered_user.fullname()
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

class Quiz(db.Model):
    """Table for quiz questions
        cp: challenge points
        cap: course access points
    """
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    question = Column(Text, nullable=False)
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

# class CoursePurchase(db.Model):
#     pass

# class Withdrawal(db.Model):
#     pass

# class EnrolledCourse(db.Model):
#     pass
