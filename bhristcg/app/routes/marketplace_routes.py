#Marketplace Routes
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from app import db
from app.models.listing import Listing, CartItem, Transaction, ALLOWED_CONDITIONS, ALLOWED_FINISHES
from app.models.card import Card
from app.services import pricing_service
from app.services.mock_data_service import MOCK_SETS, MOCK_RARITIES, MOCK_FINISHES

marketplace_bp = Blueprint('marketplace', __name__)

ALLOWED_SORT = {'newest', 'price_asc', 'price_desc', 'name'}


@marketplace_bp.route('/')
def home():
    """Render the home page with featured card listings."""
    listings = Listing.query.filter_by(status='active').order_by(
        Listing.created_at.desc()).limit(10).all()
    return render_template('home.html', listings=listings)


@marketplace_bp.route('/marketplace')
def marketplace():
    """With this you can browse listings with the search, filter by set/rarity, sort, and pagination :> """
    query = request.args.get('q', '').strip()[:128]
    set_filter = request.args.get('set', '').strip()
    rarity_filter = request.args.get('rarity', '').strip()
    finish_filter = request.args.get('finish', '').strip()
    game_filter = request.args.get('game', 'pokemon').strip()
    in_stock = request.args.get('in_stock', '')
    sort = request.args.get('sort', 'newest').strip()
    page = max(1, request.args.get('page', 1, type=int))

    if sort not in ALLOWED_SORT:
        sort = 'newest'

    listings_q = Listing.query.filter_by(status='active').join(Card)

    if game_filter:
        listings_q = listings_q.filter(Card.game == game_filter)
    if query:
        listings_q = listings_q.filter(Card.name.ilike(f'%{query}%'))
    if set_filter:
        listings_q = listings_q.filter(Card.set_name == set_filter)
    if rarity_filter:
        listings_q = listings_q.filter(Card.rarity == rarity_filter)
    if finish_filter and finish_filter in ALLOWED_FINISHES:
        listings_q = listings_q.filter(Listing.finish == finish_filter)
    if in_stock:
        listings_q = listings_q.filter(Listing.quantity > 0)

    if sort == 'price_asc':
        listings_q = listings_q.order_by(Listing.price.asc())
    elif sort == 'price_desc':
        listings_q = listings_q.order_by(Listing.price.desc())
    elif sort == 'name':
        listings_q = listings_q.order_by(Card.name.asc())
    else:
        listings_q = listings_q.order_by(Listing.created_at.desc())

    pagination = listings_q.paginate(page=page, per_page=20, error_out=False)

    sets = _get_sets()
    rarities = _get_rarities()

    return render_template(
        'marketplace.html',
        listings=pagination.items,
        pagination=pagination,
        sets=sets, rarities=rarities, finishes=MOCK_FINISHES,
        query=query, set_filter=set_filter, rarity_filter=rarity_filter,
        finish_filter=finish_filter, game_filter=game_filter,
        in_stock=in_stock, sort=sort,
    )


@marketplace_bp.route('/card/<card_id>')
def card_detail(card_id):
    """This will show the full card details and all the active listings for that card with a price suggestion """
    if len(card_id) > 128:
        abort(404)
    card = Card.query.get(card_id)
    if not card:
        abort(404)
    listings = Listing.query.filter_by(card_id=card_id, status='active').order_by(
        Listing.price.asc()).all()
    condition = request.args.get('condition', 'near_mint')
    price_suggestion = pricing_service.get_price_suggestion(card, condition)
    return render_template('card_detail.html', card=card, listings=listings,
                           price_suggestion=price_suggestion, selected_condition=condition)


@marketplace_bp.route('/api/price-suggestion')
def api_price_suggestion():
    card_id = request.args.get('card_id', '').strip()[:128]
    condition = request.args.get('condition', 'near_mint').strip()
    if condition not in ALLOWED_CONDITIONS:
        condition = 'near_mint'
    card = Card.query.get(card_id) if card_id else None
    return jsonify(pricing_service.get_price_suggestion(card, condition))


@marketplace_bp.route('/cart')
@login_required
def cart():
    """This will show the current loggedin user's card with the valid active listings and the cost summary"""
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    valid = [i for i in items if i.listing and i.listing.status == 'active']
    subtotal = sum(i.listing.price for i in valid)
    shipping = max((i.listing.shipping_cost for i in valid), default=0.0)
    return render_template('cart.html', items=valid, subtotal=subtotal, shipping=shipping)


@marketplace_bp.route('/cart/add/<int:listing_id>', methods=['POST'])
@login_required
def add_to_cart(listing_id):
    """You are able to add listings to the cart with this it also prevents you from buying own listings or any sold items"""
    listing = Listing.query.get_or_404(listing_id)
    if listing.seller_id == current_user.id:
        return jsonify({'error': 'Cannot buy your own listing.'}), 400
    if listing.status != 'active':
        return jsonify({'error': 'Listing no longer available.'}), 400
    existing = CartItem.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if not existing:
        db.session.add(CartItem(user_id=current_user.id, listing_id=listing_id))
        db.session.commit()
    return jsonify({'success': True})


@marketplace_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('marketplace.cart'))


@marketplace_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """This will be handling the purchase process of the cart items it also creates transaction record and it will notify the sellers."""
    delivery = request.form.get('delivery_type', 'shipped')
    if delivery not in ('shipped', 'pickup'):
        delivery = 'shipped'
    address = request.form.get('shipping_address', '').strip()[:500]

    try:
        item_ids = [int(i) for i in request.form.getlist('item_ids')]
    except (ValueError, TypeError):
        flash('Invalid cart data.', 'danger')
        return redirect(url_for('marketplace.cart'))

    items = CartItem.query.filter(
        CartItem.id.in_(item_ids), CartItem.user_id == current_user.id
    ).all()

    if not items:
        flash('No valid items to purchase.', 'danger')
        return redirect(url_for('marketplace.cart'))

    from datetime import datetime
    from app.models.message import Notification
    from app import socketio

    completed = []
    for item in items:
        listing = item.listing
        if not listing or listing.status != 'active' or listing.seller_id == current_user.id:
            continue
        listing.status = 'sold'
        listing.sold_at = datetime.utcnow()
        tx = Transaction(
            listing_id=listing.id, buyer_id=current_user.id,
            seller_id=listing.seller_id, amount=listing.price,
            shipping_cost=listing.shipping_cost if delivery == 'shipped' else 0,
            delivery_type=delivery,
            shipping_address=address if delivery == 'shipped' else None,
        )
        db.session.add(tx)
        db.session.delete(item)
        completed.append(listing)
        notif = Notification(
            user_id=listing.seller_id, type='sale',
            title='Card Sold!',
            body=f'{listing.card.name} — NZ${listing.price:.2f}',
            link=url_for('store.my_store'),
        )
        db.session.add(notif)

    db.session.commit()
    for listing in completed:
        socketio.emit('notification', {
            'type': 'sale', 'title': 'Card Sold!',
            'body': f'{listing.card.name} — NZ${listing.price:.2f}',
        }, room=f'user_{listing.seller_id}')

    flash(f'{len(completed)} item(s) purchased successfully!', 'success')
    return redirect(url_for('marketplace.home'))


def _get_sets():
    """This will return the distinct card sets from the active listings falling back to the mock data."""
    from sqlalchemy import distinct
    rows = db.session.query(distinct(Card.set_name)).join(
        Listing, Listing.card_id == Card.id).filter(Listing.status == 'active').all()
    result = [r[0] for r in rows if r[0]]
    return result or MOCK_SETS


def _get_rarities():
    """This will also return distinct rarities from the active listings falling back to the mock data created"""
    from sqlalchemy import distinct
    rows = db.session.query(distinct(Card.rarity)).join(
        Listing, Listing.card_id == Card.id).filter(Listing.status == 'active').all()
    result = [r[0] for r in rows if r[0]]
    return result or MOCK_RARITIES
