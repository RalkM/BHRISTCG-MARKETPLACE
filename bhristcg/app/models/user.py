#Users
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_url = db.Column(db.String(256), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    store_name = db.Column(db.String(100), nullable=True)
    store_description = db.Column(db.String(500), nullable=True)
    store_balance = db.Column(db.Float, default=0.0)
    incoming_funds = db.Column(db.Float, default=0.0)

    listings = db.relationship('Listing', backref='seller', lazy='dynamic',
                               foreign_keys='Listing.seller_id')
    collections = db.relationship('Collection', backref='owner', lazy='dynamic')
    collection_items = db.relationship('CollectionItem', backref='owner', lazy='dynamic')
    reviews_received = db.relationship('Review', backref='seller', lazy='dynamic',
                                       foreign_keys='Review.seller_id')
    reviews_given = db.relationship('Review', backref='reviewer', lazy='dynamic',
                                    foreign_keys='Review.reviewer_id')
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic',
                                    foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='recipient', lazy='dynamic',
                                        foreign_keys='Message.recipient_id')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def average_rating(self):
        reviews = self.reviews_received.all()
        if not reviews:
            return 0.0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews_received.count()

    @property
    def active_listing_count(self):
        return self.listings.filter_by(status='active').count()

    @property
    def listed_value(self):
        active = self.listings.filter_by(status='active').all()
        return sum(l.price for l in active)

    @property
    def total_revenue(self):
        from app.models.listing import Transaction
        return sum(t.amount for t in Transaction.query.filter_by(seller_id=self.id).all())

    @property
    def total_sales(self):
        from app.models.listing import Transaction
        return Transaction.query.filter_by(seller_id=self.id).count()

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
