#Review routes
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.review import Review, Report
from app.models.user import User
from app.utils.validators import ReviewForm, ReportForm
from app.utils.security import sanitize

review_bp = Blueprint('review', __name__)


@review_bp.route('/review/<int:seller_id>', methods=['GET', 'POST'])
@login_required
def leave_review(seller_id):
    seller = User.query.get_or_404(seller_id)
    if seller_id == current_user.id:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            seller_id=seller_id, reviewer_id=current_user.id,
            rating=int(form.rating.data),
            comment=sanitize(form.comment.data or '', 1000),
        )
        db.session.add(review)
        from app.models.message import Notification
        db.session.add(Notification(
            user_id=seller_id, type='review',
            title=f'New review from {current_user.username}',
            body=f'{form.rating.data}★',
            link=url_for('store.store', username=seller.username),
        ))
        db.session.commit()
        flash('Review submitted!', 'success')
        return redirect(url_for('store.store', username=seller.username))
    return render_template('review/leave_review.html', form=form, seller=seller)


@review_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    listing_id = request.args.get('listing_id', type=int)
    user_id = request.args.get('user_id', type=int)
    form = ReportForm()
    if form.validate_on_submit():
        db.session.add(Report(
            reporter_id=current_user.id,
            reported_listing_id=listing_id,
            reported_user_id=user_id,
            reason=form.reason.data,
            details=sanitize(form.details.data or '', 1000),
        ))
        db.session.commit()
        flash('Report submitted. Our team will review it.', 'success')
        return redirect(url_for('marketplace.marketplace'))
    return render_template('review/report.html', form=form,
                           listing_id=listing_id, user_id=user_id)
