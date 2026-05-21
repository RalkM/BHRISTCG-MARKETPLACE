from datetime import datetime
from app import db


class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    cover_image = db.Column(db.String(512), nullable=True)
    total_cards_needed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('CollectionItem', backref='collection',
                            lazy='dynamic', cascade='all, delete-orphan',
                            foreign_keys='CollectionItem.collection_id')

    @property
    def total_owned(self):
        return sum(i.quantity for i in self.items.all())

    @property
    def total_value(self):
        return round(sum(i.current_market_value for i in self.items.all()), 2)

    @property
    def card_count_label(self):
        owned = self.total_owned
        needed = self.total_cards_needed
        if needed:
            return f'{owned}/{needed} Cards'
        return f'{owned} Cards'

    def __repr__(self):
        return f'<Collection {self.name}>'


class CollectionItem(db.Model):
    __tablename__ = 'collection_items'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=True)
    card_id = db.Column(db.String(64), db.ForeignKey('cards.id'), nullable=False)
    condition = db.Column(db.String(32), default='near_mint')
    finish = db.Column(db.String(32), default='non_holo')
    quantity = db.Column(db.Integer, default=1)
    purchase_price = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def current_market_value(self):
        if not self.card or not self.card.market_price:
            return (self.purchase_price or 0.0) * self.quantity
        from app.services.pricing_service import get_condition_multiplier
        return round(self.card.market_price * get_condition_multiplier(self.condition) * self.quantity, 2)

    def __repr__(self):
        return f'<CollectionItem {self.card_id}>'
