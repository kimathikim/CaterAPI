import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration variables."""

    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DEBUG = os.getenv('DEBUG', False)

    # Database
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PWD = os.getenv('MYSQL_PWD', 'password')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.getenv('MYSQL_DB', 'catering_db')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in [
        'true', '1', 't']
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in [
        'true', '1', 't']
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER", "briankimathi94@gmail.com")

    # Redis Config for Celery
    REDIS_URI = os.getenv('REDIS_URI', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URI
    CELERY_RESULT_BACKEND = REDIS_URI

    # JWT Config
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
