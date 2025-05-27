"""
Tag related DTOs and schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_schemas import BaseResponse


class TagRequest(BaseModel):
    """Schema for incoming tag creation requests"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(min_length=1, max_length=100, description="Tag name")
    description: Optional[str] = Field(default=None, description="Tag description")
    type: Optional[str] = Field(default=None, description="Tag type")
    trigger: Optional[str] = Field(default=None, description="Tag trigger condition")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Tag configuration")


class TagResponse(BaseModel):
    """Schema for tag response"""
    id: int = Field(description="Tag ID")
    name: str = Field(description="Tag name")
    description: Optional[str] = Field(default=None, description="Tag description")
    type: Optional[str] = Field(default=None, description="Tag type")
    trigger: Optional[str] = Field(default=None, description="Tag trigger condition")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Tag configuration")
    created_at: datetime = Field(description="Creation timestamp")


class TagCreateResponse(BaseResponse):
    """Response for created tag"""
    tag_id: int = Field(description="Created tag ID")


class TagsListResponse(BaseModel):
    """Response for tags list"""
    tags: List[TagResponse] = Field(description="List of tags")
