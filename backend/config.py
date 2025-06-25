import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Flask configuration class"""
    
    # Database settings
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_NAME = os.getenv('POSTGRES_DB', 'analytics')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASS = os.getenv('POSTGRES_PASSWORD', 'tobias')
    DB_PORT = os.getenv('POSTGRES_PORT', '6666')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False') == 'True'
    
    # Flask settings
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
      # Server settings
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # API settings
    API_BASE_URL = os.getenv('API_BASE_URL', f'http://localhost:{PORT}')


# Legacy compatibility - keep old variables for existing code
DB_HOST = Config.DB_HOST
DB_NAME = Config.DB_NAME
DB_USER = Config.DB_USER
DB_PASS = Config.DB_PASS
DB_PORT = Config.DB_PORT
DEBUG = Config.DEBUG
PORT = Config.PORT
HOST = Config.HOST
DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI
