import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        'super_secret_key_for_hbnb_project_very_long_and_secure_123456789'
    )
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
