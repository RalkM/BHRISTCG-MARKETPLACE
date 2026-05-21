#Store routes
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.listing import Listing, Transaction
from app.models.review import Review
from app.utils.validators import ProfileForm
from app.utils.security import sanitize

store_bp = Blueprint('store', __name__)


@store_bp.route('/store/<username>')
def store(username):
    seller = User.query.filter_by(username=username).first_or_404()
    listings = Listing.query.filter_by(seller_id=seller.id, status='active').order_by(
        Listing.created_at.desc()).all()
    reviews = Review.query.filter_by(seller_id=seller.id).order_by(
        Review.created_at.desc()).limit(10).all()
    total_sold = Listing.query.filter_by(seller_id=seller.id, status='sold').count()
    return render_template('store/store.html', seller=seller, listings=listings,
                           reviews=reviews, total_sold=total_sold)


@store_bp.route('/my-store')
@login_required
def my_store():
    active = Listing.query.filter_by(seller_id=current_user.id, status='active').order_by(
        Listing.created_at.desc()).all()
    sold = Listing.query.filter_by(seller_id=current_user.id, status='sold').order_by(
        Listing.sold_at.desc()).limit(20).all()
    return render_template('store/my_store.html',
                           active_listings=active, sold_listings=sold)


@store_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.store_name = sanitize(form.store_name.data or '', 100) or None
        current_user.store_description = sanitize(form.store_description.data or '', 500) or None
        current_user.bio = sanitize(form.bio.data or '', 500) or None
        current_user.location = sanitize(form.location.data or '', 100) or None
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('store.my_store'))
    return render_template('store/edit_profile.html', form=form)
