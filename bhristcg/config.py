#config
import os
from dotenv import load_dotenv

# Loading the environment variables from .env for local development
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-secret-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bhristcg.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POKEMON_TCG_API_KEY = os.environ.get('POKEMON_TCG_API_KEY', '').strip()
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))
    MAX_MESSAGE_LENGTH = 1000
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
