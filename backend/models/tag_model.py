"""
Tag model using SQLAlchemy ORM instead of raw SQL
"""
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from models.db_models import Tag
from models.db_instance import db
import logging

logger = logging.getLogger(__name__)

def create_tag(tag_data):
    """Create a new tag using ORM"""
    try:
        # Create a new Tag object
        new_tag = Tag(
            name=tag_data.get('name'),
            description=tag_data.get('description'),
            type=tag_data.get('type'),
            trigger=tag_data.get('trigger'),
            config=tag_data.get('config', {}),
            is_active=tag_data.get('is_active', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add to session and commit
        db.session.add(new_tag)
        db.session.commit()
        
        # Return the tag ID
        return new_tag.id
    except IntegrityError:
        db.session.rollback()
        logger.error(f"Tag with name '{tag_data.get('name')}' already exists")
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating tag: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating tag: {str(e)}")
        return None

def get_tag_by_id(tag_id):
    """Get a tag by ID"""
    try:
        tag = Tag.query.get(tag_id)
        return tag.to_dict() if tag else None
    except Exception as e:
        logger.error(f"Error retrieving tag by ID: {str(e)}")
        return None

def get_tag_by_name(tag_name):
    """Get a tag by name"""
    try:
        tag = Tag.query.filter_by(name=tag_name).first()
        return tag.to_dict() if tag else None
    except Exception as e:
        logger.error(f"Error retrieving tag by name: {str(e)}")
        return None

def get_all_tags(active_only=False):
    """Get all tags, optionally filtering for active only"""
    try:
        query = Tag.query
        if active_only:
            query = query.filter_by(is_active=True)
        
        tags = query.order_by(Tag.name).all()
        return [tag.to_dict() for tag in tags]
    except Exception as e:
        logger.error(f"Error retrieving tags: {str(e)}")
        return []

def update_tag(tag_id, tag_data):
    """Update an existing tag"""
    try:
        tag = Tag.query.get(tag_id)
        if not tag:
            return False
        
        # Update fields
        if 'name' in tag_data:
            tag.name = tag_data['name']
        if 'description' in tag_data:
            tag.description = tag_data['description']
        if 'type' in tag_data:
            tag.type = tag_data['type']
        if 'trigger' in tag_data:
            tag.trigger = tag_data['trigger']
        if 'config' in tag_data:
            tag.config = tag_data['config']
        if 'is_active' in tag_data:
            tag.is_active = tag_data['is_active']
        
        tag.updated_at = datetime.utcnow()
        
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        logger.error(f"Tag with name '{tag_data.get('name')}' already exists")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating tag: {str(e)}")
        return False

def delete_tag(tag_id):
    """Delete a tag by ID"""
    try:
        tag = Tag.query.get(tag_id)
        if not tag:
            return False
        
        db.session.delete(tag)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting tag: {str(e)}")
        return False
