"""
Database instance for SQLAlchemy ORM
This module holds the db instance to avoid circular imports
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()
