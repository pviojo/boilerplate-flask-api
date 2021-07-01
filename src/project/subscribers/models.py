from datetime import datetime

from project import db

from project.common.model import Model


class Subscriber(Model):
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hash = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=False, nullable=False, index=True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    status = db.Column(db.String(255), unique=False, nullable=False, index=True, default='PENDING')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

