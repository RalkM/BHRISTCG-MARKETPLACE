#Messages
from datetime import datetime
from app import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=True)
    body = db.Column(db.String(1000), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listing = db.relationship('Listing', foreign_keys=[listing_id])

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_username': self.sender.username if self.sender else '',
            'recipient_id': self.recipient_id,
            'body': self.body,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%H:%M'),
            'created_date': self.created_at.strftime('%b %d'),
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(256), nullable=True)
    link = db.Column(db.String(256), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'body': self.body,
            'link': self.link,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }
