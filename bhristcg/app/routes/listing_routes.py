#Listing Routes
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.listing import Listing, ALLOWED_CONDITIONS, ALLOWED_FINISHES
from app.models.card import Card
from app.services import pricing_service
from app.utils.validators import ListingForm
from app.utils.security import check_owner, sanitize

listing_bp = Blueprint('listing', __name__)


@listing_bp.route('/listing/new', methods=['GET', 'POST'])
@login_required
def new_listing():
    """Search for a card then create a listing for it."""
    form = ListingForm()
    search_query = request.args.get('q', '').strip()[:128]
    card_id = request.args.get('card_id', '').strip()[:128]
    selected_card = Card.query.get(card_id) if card_id else None
    price_suggestion = None

    if selected_card:
        price_suggestion = pricing_service.get_price_suggestion(selected_card, 'near_mint')

    if form.validate_on_submit():
        if form.condition.data not in ALLOWED_CONDITIONS:
            flash('Invalid condition.', 'danger')
            return redirect(url_for('listing.new_listing'))
        if form.finish.data not in ALLOWED_FINISHES:
            flash('Invalid finish.', 'danger')
            return redirect(url_for('listing.new_listing'))

        card = Card.query.get(form.card_id.data.strip())
        if not card:
            flash('Card not found.', 'danger')
            return redirect(url_for('listing.new_listing'))

        listing = Listing(
            card_id=card.id,
            seller_id=current_user.id,
            price=round(form.price.data, 2),
            condition=form.condition.data,
            finish=form.finish.data,
            notes=sanitize(form.notes.data or '', 1000),
            quantity=max(1, min(100, form.quantity.data or 1)),
            delivery_type=form.delivery_type.data,
            shipping_cost=round(form.shipping_cost.data or 10.0, 2),
            status='active',
        )
        db.session.add(listing)
        db.session.commit()
        flash('Listing created successfully!', 'success')
        return redirect(url_for('store.my_store'))

    cards = []
    if search_query:
        cards = Card.query.filter(Card.name.ilike(f'%{search_query}%')).limit(20).all()

    return render_template('listing/new_listing.html',
                           form=form, search_query=search_query,
                           cards=cards, selected_card=selected_card,
                           price_suggestion=price_suggestion)


@listing_bp.route('/listing/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    check_owner(listing)
    form = ListingForm(obj=listing)
    if form.validate_on_submit():
        if form.condition.data not in ALLOWED_CONDITIONS:
            flash('Invalid condition.', 'danger')
            return render_template('listing/edit_listing.html', form=form, listing=listing)
        listing.price = round(form.price.data, 2)
        listing.condition = form.condition.data
        listing.finish = form.finish.data
        listing.notes = sanitize(form.notes.data or '', 1000)
        listing.quantity = max(1, min(100, form.quantity.data or 1))
        listing.delivery_type = form.delivery_type.data
        listing.shipping_cost = round(form.shipping_cost.data or 10.0, 2)
        db.session.commit()
        flash('Listing updated.', 'success')
        return redirect(url_for('store.my_store'))
    return render_template('listing/edit_listing.html', form=form, listing=listing)


@listing_bp.route('/listing/<int:listing_id>/remove', methods=['POST'])
@login_required
def remove_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    check_owner(listing)
    listing.status = 'removed'
    db.session.commit()
    flash('Listing removed.', 'info')
    return redirect(url_for('store.my_store'))
