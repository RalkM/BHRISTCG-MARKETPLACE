# Initializes the Flask application and extensions
# Will configure routes, database, and SocketIO
# Sets up the main Flask app, connects extensions, registers routes, and prepares the database.
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, async_mode='threading',
                      cors_allowed_origins='*',
                      logger=False, engineio_logger=False)

    from app.routes.auth_routes import auth_bp
    from app.routes.marketplace_routes import marketplace_bp
    from app.routes.listing_routes import listing_bp
    from app.routes.collection_routes import collection_bp
    from app.routes.chat_routes import chat_bp
    from app.routes.review_routes import review_bp
    from app.routes.store_routes import store_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(store_bp)

    from app.routes.chat_routes import register_socketio_events
    register_socketio_events(socketio)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f'Server error: {e}')
        return render_template('errors/500.html'), 500

    # Ensure the database and mock data exist when the app starts.
    # This is a simple startup pattern used in the NZFTC-inspired project.
    with app.app_context():
        db.create_all()
        from app.services.mock_data_service import seed_if_empty
        seed_if_empty()

    return app
