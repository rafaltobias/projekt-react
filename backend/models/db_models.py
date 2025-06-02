"""
SQLAlchemy ORM models for the analytics application
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Import db instance from db_instance to avoid circular imports
from models.db_instance import db


class Visit(db.Model):
    """Model for tracking website visits"""
    __tablename__ = 'visits'
    
    id = Column(Integer, primary_key=True)
    page_url = Column(String(500), nullable=False, index=True)
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    referrer = Column(String(500))
    browser = Column(String(100))
    os = Column(String(100))
    device = Column(String(100))
    country = Column(String(100))
    session_id = Column(String(255), index=True)
    is_entry_page = Column(Boolean, default=False)
    is_exit_page = Column(Boolean, default=False)
    event_name = Column(String(255))
    event_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Visit id={self.id} page={self.page_url} session={self.session_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'page_url': self.page_url,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'browser': self.browser,
            'os': self.os,
            'device': self.device,
            'country': self.country,
            'session_id': self.session_id,
            'is_entry_page': self.is_entry_page,
            'is_exit_page': self.is_exit_page,
            'event_name': self.event_name,
            'event_data': self.event_data,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }


class TrackingEvent(db.Model):
    """Model for tracking events (page views and custom events)"""
    __tablename__ = 'tracking_events'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, index=True)
    page_url = Column(String(500), nullable=False, index=True)
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    referrer = Column(String(500))
    browser = Column(String(100))
    os = Column(String(100))
    device = Column(String(100))
    country = Column(String(100))
    city = Column(String(100))
    is_entry_page = Column(Boolean, default=False)
    is_exit_page = Column(Boolean, default=False)
    event_name = Column(String(255))
    event_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<TrackingEvent id={self.id} event={self.event_name} session={self.session_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'page_url': self.page_url,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'browser': self.browser,
            'os': self.os,
            'device': self.device,
            'country': self.country,
            'city': self.city,
            'is_entry_page': self.is_entry_page,
            'is_exit_page': self.is_exit_page,
            'event_name': self.event_name,
            'event_data': self.event_data,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }


class Tag(db.Model):
    """Model for tags management"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    type = Column(String(50))
    trigger = Column(String(255))
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Tag id={self.id} name={self.name} type={self.type}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'trigger': self.trigger,
            'config': self.config,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'is_active': self.is_active
        }
