from datetime import datetime
from app import db


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    set_name = db.Column(db.String(128), nullable=False)
    set_id = db.Column(db.String(64), nullable=True)
    number = db.Column(db.String(20), nullable=True)
    rarity = db.Column(db.String(64), nullable=True)
    types = db.Column(db.String(128), nullable=True)
    supertype = db.Column(db.String(64), nullable=True)
    subtypes = db.Column(db.String(128), nullable=True)
    hp = db.Column(db.String(16), nullable=True)
    image_url = db.Column(db.String(512), nullable=True)
    image_url_hi = db.Column(db.String(512), nullable=True)
    game = db.Column(db.String(32), default='pokemon')

    market_price = db.Column(db.Float, nullable=True)
    low_price = db.Column(db.Float, nullable=True)
    high_price = db.Column(db.Float, nullable=True)
    mid_price = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship('Listing', backref='card', lazy='dynamic')
    collection_items = db.relationship('CollectionItem', backref='card', lazy='dynamic')

    def __repr__(self):
        return f'<Card {self.name}>'
