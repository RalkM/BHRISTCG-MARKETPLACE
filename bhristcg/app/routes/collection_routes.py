#Collection Routes
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.collection import Collection, CollectionItem
from app.models.card import Card
from app.utils.validators import CollectionForm
from app.utils.security import sanitize

collection_bp = Blueprint('collection', __name__)


@collection_bp.route('/collections')
@login_required
def collections():
    user_collections = Collection.query.filter_by(owner_id=current_user.id).all()
    all_items = CollectionItem.query.filter_by(owner_id=current_user.id).all()

    total_value = round(sum(i.current_market_value for i in all_items), 2)
    total_owned = sum(i.quantity for i in all_items)
    total_needed = sum(c.total_cards_needed for c in user_collections)
    needed_value = sum(
        (c.total_cards_needed - c.total_owned) * 15  # avg placeholder
        for c in user_collections if c.total_cards_needed > c.total_owned
    )

    return render_template('collection/collections.html',
                           collections=user_collections,
                           total_value=total_value,
                           total_owned=total_owned,
                           total_needed=total_needed,
                           needed_value=round(needed_value, 2))


@collection_bp.route('/collections/new', methods=['GET', 'POST'])
@login_required
def new_collection():
    form = CollectionForm()
    if form.validate_on_submit():
        coll = Collection(
            owner_id=current_user.id,
            name=sanitize(form.name.data, 100),
            description=sanitize(form.description.data or '', 500),
            total_cards_needed=form.total_cards_needed.data or 0,
        )
        db.session.add(coll)
        db.session.commit()
        flash('Collection created!', 'success')
        return redirect(url_for('collection.collections'))
    return render_template('collection/new_collection.html', form=form)


@collection_bp.route('/collections/<int:collection_id>')
@login_required
def view_collection(collection_id):
    coll = Collection.query.get_or_404(collection_id)
    if coll.owner_id != current_user.id:
        abort(403)
    items = coll.items.all()
    return render_template('collection/view_collection.html', collection=coll, items=items)


@collection_bp.route('/collections/<int:collection_id>/add', methods=['GET', 'POST'])
@login_required
def add_to_collection(collection_id):
    coll = Collection.query.get_or_404(collection_id)
    if coll.owner_id != current_user.id:
        abort(403)

    search_query = request.args.get('q', '').strip()[:128]
    card_id = request.args.get('card_id', '').strip()[:128]
    selected_card = Card.query.get(card_id) if card_id else None

    if request.method == 'POST':
        c_id = request.form.get('card_id', '').strip()
        condition = request.form.get('condition', 'near_mint')
        finish = request.form.get('finish', 'non_holo')
        qty = max(1, min(9999, int(request.form.get('quantity', 1) or 1)))
        purchase_price = request.form.get('purchase_price', '')
        try:
            purchase_price = float(purchase_price) if purchase_price else None
        except ValueError:
            purchase_price = None

        card = Card.query.get(c_id)
        if not card:
            flash('Card not found.', 'danger')
            return redirect(url_for('collection.add_to_collection', collection_id=collection_id))

        existing = CollectionItem.query.filter_by(
            owner_id=current_user.id, collection_id=collection_id,
            card_id=c_id, condition=condition, finish=finish).first()
        if existing:
            existing.quantity += qty
        else:
            item = CollectionItem(
                owner_id=current_user.id, collection_id=collection_id,
                card_id=c_id, condition=condition, finish=finish,
                quantity=qty, purchase_price=purchase_price,
            )
            db.session.add(item)

        db.session.commit()
        flash('Card added to collection!', 'success')
        return redirect(url_for('collection.view_collection', collection_id=collection_id))

    cards = []
    if search_query:
        cards = Card.query.filter(Card.name.ilike(f'%{search_query}%')).limit(20).all()

    return render_template('collection/add_to_collection.html',
                           collection=coll, search_query=search_query,
                           cards=cards, selected_card=selected_card)


@collection_bp.route('/collections/item/<int:item_id>/remove', methods=['POST'])
@login_required
def remove_item(item_id):
    item = CollectionItem.query.get_or_404(item_id)
    if item.owner_id != current_user.id:
        abort(403)
    coll_id = item.collection_id
    db.session.delete(item)
    db.session.commit()
    flash('Card removed from collection.', 'info')
    return redirect(url_for('collection.view_collection', collection_id=coll_id))


@collection_bp.route('/api/collection/value')
@login_required
def collection_value():
    items = CollectionItem.query.filter_by(owner_id=current_user.id).all()
    total = round(sum(i.current_market_value for i in items), 2)
    return jsonify({'total_value': total, 'count': len(items)})
