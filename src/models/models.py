from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from the database module
from src.database import db

class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500), nullable=False)
    referrer = db.Column(db.String(500))
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))
    browser = db.Column(db.Text)
    os = db.Column(db.Text)
    device = db.Column(db.Text)
    country = db.Column(db.Text)
    is_entry_page = db.Column(db.Boolean, default=False)
    is_exit_page = db.Column(db.Boolean, default=False)
    tags = db.Column(db.JSON)  # This matches the 'tags' column in the DB (jsonb type)
    event_name = db.Column(db.Text)
    event_data = db.Column(db.JSON)
    
    # No direct relationship with Tag table - we're using a JSONB field instead
    
    def to_dict(self):
        return {
            'id': self.id,
            'page_url': self.page_url,
            'referrer': self.referrer,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'session_id': self.session_id,
            'browser': self.browser,
            'os': self.os,
            'device': self.device,
            'country': self.country,
            'is_entry_page': self.is_entry_page,
            'is_exit_page': self.is_exit_page,
            'tags': self.tags,
            'event_name': self.event_name,
            'event_data': self.event_data
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    trigger_condition = db.Column(db.Text)
    tag_content = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    type = db.Column(db.Text)
    config = db.Column(db.Text)
    trigger = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trigger_condition': self.trigger_condition,
            'tag_content': self.tag_content,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'type': self.type,
            'config': self.config,
            'trigger': self.trigger
        }

class StatsView(db.Model):
    """Model for storing aggregated statistics"""
    __tablename__ = 'stats_view'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    page_url = db.Column(db.String(500))
    visit_count = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'page_url': self.page_url,
            'visit_count': self.visit_count,
            'unique_visitors': self.unique_visitors
        }
