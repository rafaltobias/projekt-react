"""
Tag management service - business logic for tags
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import desc
from models.db_instance import db
from models.db_models import Tag
from services.base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class TagService(BaseService):
    """Service for tag management operations"""
    
    @staticmethod
    def create_tag(
        name: str,
        description: Optional[str] = None,
        type: Optional[str] = None,
        trigger: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        """Create a new tag"""
        try:
            # Check if tag with this name already exists
            existing_tag = Tag.query.filter_by(name=name).first()
            if existing_tag:
                logger.warning(f"Tag with name '{name}' already exists")
                raise ValueError(f"Tag with name '{name}' already exists")
            
            tag = Tag(
                name=name,
                description=description,
                type=type,
                trigger=trigger,
                config=config
            )
            
            db.session.add(tag)
            TagService.commit_changes()
            
            logger.info(f"Created tag {tag.id}: {name}")
            return tag.id
            
        except Exception as e:
            TagService.handle_db_error("create_tag", e)
            return None
    
    @staticmethod
    def get_all_tags(include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all tags"""
        try:
            query = Tag.query
            if not include_inactive:
                query = query.filter_by(is_active=True)
            
            tags = query.order_by(Tag.name).all()
            return [tag.to_dict() for tag in tags]
            
        except Exception as e:
            logger.error(f"Error getting tags: {str(e)}")
            return []
    
    @staticmethod
    def get_tag_by_id(tag_id: int) -> Optional[Dict[str, Any]]:
        """Get tag by ID"""
        try:
            tag = Tag.query.get(tag_id)
            return tag.to_dict() if tag else None
        except Exception as e:
            logger.error(f"Error getting tag {tag_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_tag_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Get tag by name"""
        try:
            tag = Tag.query.filter_by(name=name).first()
            return tag.to_dict() if tag else None
        except Exception as e:
            logger.error(f"Error getting tag by name '{name}': {str(e)}")
            return None
    
    @staticmethod
    def update_tag(
        tag_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        trigger: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None
    ) -> bool:
        """Update an existing tag"""
        try:
            tag = Tag.query.get(tag_id)
            if not tag:
                logger.warning(f"Tag {tag_id} not found for update")
                return False
            
            # Check for name conflicts if name is being changed
            if name and name != tag.name:
                existing_tag = Tag.query.filter_by(name=name).first()
                if existing_tag:
                    logger.warning(f"Tag with name '{name}' already exists")
                    raise ValueError(f"Tag with name '{name}' already exists")
                tag.name = name
            
            if description is not None:
                tag.description = description
            if type is not None:
                tag.type = type
            if trigger is not None:
                tag.trigger = trigger
            if config is not None:
                tag.config = config
            if is_active is not None:
                tag.is_active = is_active
            
            tag.updated_at = datetime.utcnow()
            
            TagService.commit_changes()
            logger.info(f"Updated tag {tag_id}: {tag.name}")
            return True
            
        except Exception as e:
            TagService.handle_db_error("update_tag", e)
            return False
    
    @staticmethod
    def delete_tag(tag_id: int, soft_delete: bool = True) -> bool:
        """Delete a tag (soft delete by default)"""
        try:
            tag = Tag.query.get(tag_id)
            if not tag:
                logger.warning(f"Tag {tag_id} not found for deletion")
                return False
            
            if soft_delete:
                # Soft delete - just mark as inactive
                tag.is_active = False
                tag.updated_at = datetime.utcnow()
                logger.info(f"Soft deleted tag {tag_id}: {tag.name}")
            else:
                # Hard delete - actually remove from database
                db.session.delete(tag)
                logger.info(f"Hard deleted tag {tag_id}: {tag.name}")
            
            TagService.commit_changes()
            return True
            
        except Exception as e:
            TagService.handle_db_error("delete_tag", e)
            return False
    
    @staticmethod
    def get_tags_by_type(tag_type: str) -> List[Dict[str, Any]]:
        """Get tags by type"""
        try:
            tags = Tag.query.filter_by(type=tag_type, is_active=True).order_by(Tag.name).all()
            return [tag.to_dict() for tag in tags]
        except Exception as e:
            logger.error(f"Error getting tags by type '{tag_type}': {str(e)}")
            return []
