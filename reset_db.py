"""
Script to reset the database and initialize with basic schema
"""
import os
from flask import Flask
from dotenv import load_dotenv
from src.database import db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

# Get database connection parameters
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_db = os.environ.get('POSTGRES_DB', 'analytics')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'tobias')
postgres_port = os.environ.get('POSTGRES_PORT', '6666')

print("Starting database reset process...")

# Create a temporary app context for SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import models to ensure they're registered
from src.models.models import Visit, Tag, StatsView

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating tables based on models...")
    db.create_all()
    
    print("Creating initial tags...")
    default_tags = [
        Tag(name="Homepage", description="Main page of the website", color="#3B82F6"),
        Tag(name="Blog", description="Blog posts", color="#10B981"),
        Tag(name="Products", description="Product catalog", color="#F59E0B"),
        Tag(name="Checkout", description="Checkout process", color="#EF4444")
    ]
    
    db.session.add_all(default_tags)
    db.session.commit()
    
    print("Database reset complete!")