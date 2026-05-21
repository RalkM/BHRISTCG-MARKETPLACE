#Reviews
from datetime import datetime
from app import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transaction = db.relationship('Transaction', foreign_keys=[transaction_id])


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reported_listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=True)
    reason = db.Column(db.String(64), nullable=False)
    details = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(32), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reporter = db.relationship('User', foreign_keys=[reporter_id])
    reported_user = db.relationship('User', foreign_keys=[reported_user_id])
    reported_listing = db.relationship('Listing', foreign_keys=[reported_listing_id])
