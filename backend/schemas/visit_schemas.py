"""
Visit related DTOs and schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_schemas import BaseResponse


class VisitRequest(BaseModel):
    """Schema for incoming visit tracking requests"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    page_url: str = Field(description="URL of the page being visited")
    referrer: Optional[str] = Field(default=None, description="Referrer URL")
    browser: Optional[str] = Field(default=None, description="Browser name")
    os: Optional[str] = Field(default=None, description="Operating system")
    device: Optional[str] = Field(default=None, description="Device type")
    country: Optional[str] = Field(default=None, description="Country code")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    is_entry_page: bool = Field(default=False, description="Whether this is an entry page")
    is_exit_page: bool = Field(default=False, description="Whether this is an exit page")
    event_name: Optional[str] = Field(default=None, description="Custom event name")
    event_data: Optional[Dict[str, Any]] = Field(default=None, description="Custom event data")


class VisitResponse(BaseModel):
    """Schema for visit response"""
    id: int = Field(description="Visit ID")
    page_url: str = Field(description="Page URL")
    ip_address: Optional[str] = Field(default=None, description="IP address")
    user_agent: Optional[str] = Field(default=None, description="User agent")
    referrer: Optional[str] = Field(default=None, description="Referrer URL")
    browser: Optional[str] = Field(default=None, description="Browser name")
    os: Optional[str] = Field(default=None, description="Operating system")
    device: Optional[str] = Field(default=None, description="Device type")
    country: Optional[str] = Field(default=None, description="Country code")
    timestamp: datetime = Field(description="Visit timestamp")
    session_id: Optional[str] = Field(default=None, description="Session ID")
    is_entry_page: bool = Field(description="Whether this is an entry page")
    is_exit_page: bool = Field(description="Whether this is an exit page")
    event_name: Optional[str] = Field(default=None, description="Custom event name")
    event_data: Optional[Dict[str, Any]] = Field(default=None, description="Custom event data")


class VisitCreateResponse(BaseResponse):
    """Response for created visit"""
    visit_id: int = Field(description="Created visit ID")
    session_id: Optional[str] = Field(default=None, description="Session ID")
