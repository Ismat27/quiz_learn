from flaskr.models import db
from sqlalchemy import ForeignKey, Column, Text, String, Integer
from sqlalchemy.orm import relationship, backref


class UserProfile(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref("profile", uselist=False), foreign_keys=[user_id])
    cap = Column(Integer)
    cp = Column(Integer)
