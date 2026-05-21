#Listings
from datetime import datetime
from app import db

CONDITION_CHOICES = [
    ('mint', 'Mint'),
    ('near_mint', 'Near Mint'),
    ('light_played', 'Light Played'),
    ('played', 'Played'),
    ('damaged', 'Damaged'),
]

FINISH_CHOICES = [
    ('non_holo', 'Non-Holo'),
    ('holo', 'Holo'),
    ('reverse_holo', 'Reverse Holo'),
    ('foil', 'Foil'),
    ('sir', 'SIR'),
    ('alt_art', 'Alt Art'),
]

ALLOWED_CONDITIONS = {c[0] for c in CONDITION_CHOICES}
ALLOWED_FINISHES = {f[0] for f in FINISH_CHOICES}


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(64), db.ForeignKey('cards.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(32), nullable=False, default='near_mint')
    finish = db.Column(db.String(32), nullable=False, default='non_holo')
    notes = db.Column(db.String(1000), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(16), default='active', index=True)
    delivery_type = db.Column(db.String(16), default='both')
    shipping_cost = db.Column(db.Float, default=10.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sold_at = db.Column(db.DateTime, nullable=True)

    cart_items = db.relationship('CartItem', backref='listing', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='listing', lazy='dynamic')

    @property
    def condition_label(self):
        return dict(CONDITION_CHOICES).get(self.condition, self.condition)

    @property
    def finish_label(self):
        labels = {
            'non_holo': 'Non-Holo', 'holo': 'Holo',
            'reverse_holo': 'Rev. Holo', 'foil': 'Foil',
            'sir': 'SIR', 'alt_art': 'Alt Art',
        }
        return labels.get(self.finish, self.finish)

    def __repr__(self):
        return f'<Listing #{self.id} ${self.price}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, default=0.0)
    delivery_type = db.Column(db.String(16), nullable=False)
    shipping_address = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(32), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    buyer = db.relationship('User', foreign_keys=[buyer_id])
    seller = db.relationship('User', foreign_keys=[seller_id])
