#Authentication
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.utils.validators import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('marketplace.home'))
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email.data.strip()
        user = (User.query.filter_by(email=identifier.lower()).first() or
                User.query.filter_by(username=identifier).first())
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('marketplace.home'))
        flash('Invalid email/username or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('marketplace.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('auth/register.html', form=form)
        # Generate username from email prefix
        base = email.split('@')[0]
        username = base
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f'{base}{counter}'
            counter += 1
        user = User(username=username, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created! Welcome to BhrisTCG.', 'success')
        return redirect(url_for('marketplace.home'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('marketplace.home'))
