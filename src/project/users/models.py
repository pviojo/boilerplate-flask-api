from datetime import datetime
from sqlalchemy import Index
from flask import current_app as app
from project import db, bcrypt
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

from project.common.model import Model
from project.common.helpers import hash_with_prefix


class Relation(Model):
    """ User Model for storing user related details """
    __tablename__ = "relations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False, index=True)
    item_type = db.Column(db.String(255), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    Index('item', item_type, item_id)

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type,
            "item_id": self.item_id,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class User(Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hash = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)
        self.hash = hash_with_prefix(
            prefix='user',
            s=self.email
        )
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

        

    def json(self):
        return {
            "id": self.id,
            "hash": self.hash,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class BlacklistToken(Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(2000), unique=True, nullable=False, index=True)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
