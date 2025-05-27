"""
Tracking related DTOs and schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_schemas import BaseResponse, PaginatedResponse


class TrackingEventRequest(BaseModel):
    """Schema for incoming tracking event requests"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    session_id: str = Field(description="Unique session identifier")
    page_url: str = Field(description="URL of the page being tracked")
    referrer: Optional[str] = Field(default=None, description="Referrer URL")
    browser: Optional[str] = Field(default=None, description="Browser name")
    os: Optional[str] = Field(default=None, description="Operating system")
    device: Optional[str] = Field(default=None, description="Device type")
    country: Optional[str] = Field(default=None, description="Country code")
    city: Optional[str] = Field(default=None, description="City name")
    is_entry_page: bool = Field(default=False, description="Whether this is an entry page")
    is_exit_page: bool = Field(default=False, description="Whether this is an exit page")
    event_name: Optional[str] = Field(default=None, description="Custom event name")
    event_data: Optional[Dict[str, Any]] = Field(default=None, description="Custom event data")


class TrackingEventResponse(BaseModel):
    """Schema for tracking event response"""
    id: int = Field(description="Event ID")
    session_id: str = Field(description="Session ID")
    page_url: str = Field(description="Page URL")
    ip_address: Optional[str] = Field(default=None, description="IP address")
    user_agent: Optional[str] = Field(default=None, description="User agent")
    referrer: Optional[str] = Field(default=None, description="Referrer URL")
    browser: Optional[str] = Field(default=None, description="Browser name")
    os: Optional[str] = Field(default=None, description="Operating system")
    device: Optional[str] = Field(default=None, description="Device type")
    country: Optional[str] = Field(default=None, description="Country code")
    city: Optional[str] = Field(default=None, description="City name")
    timestamp: datetime = Field(description="Event timestamp")
    is_entry_page: bool = Field(description="Whether this is an entry page")
    is_exit_page: bool = Field(description="Whether this is an exit page")
    event_name: Optional[str] = Field(default=None, description="Custom event name")
    event_data: Optional[Dict[str, Any]] = Field(default=None, description="Custom event data")


class TrackingEventCreateResponse(BaseResponse):
    """Response for created tracking event"""
    event_id: int = Field(description="Created event ID")
    timestamp: datetime = Field(description="Event timestamp")


class TrackingEventsResponse(PaginatedResponse):
    """Response for tracking events list"""
    events: List[TrackingEventResponse] = Field(description="List of tracking events")
    type: str = Field(description="Type of events (all, page_views, custom_events)")


class SessionDataResponse(BaseModel):
    """Schema for session data response"""
    session_id: str = Field(description="Session ID")
    events: List[TrackingEventResponse] = Field(description="Events in the session")
    total_events: int = Field(description="Total number of events")
    duration: Optional[int] = Field(default=None, description="Session duration in seconds")
    entry_page: Optional[str] = Field(default=None, description="Entry page URL")
    exit_page: Optional[str] = Field(default=None, description="Exit page URL")


class SessionAnalyticsResponse(BaseModel):
    """Schema for session analytics response"""
    total_sessions: int = Field(description="Total number of sessions")
    average_session_duration: Optional[float] = Field(default=None, description="Average session duration")
    bounce_rate: Optional[float] = Field(default=None, description="Bounce rate percentage")
    top_entry_pages: List[Dict[str, Any]] = Field(description="Top entry pages")
    top_exit_pages: List[Dict[str, Any]] = Field(description="Top exit pages")


class TrackingStatsResponse(BaseModel):
    """Schema for tracking statistics response"""
    total_page_views: int = Field(description="Total page views")
    total_custom_events: int = Field(description="Total custom events")
    unique_sessions: int = Field(description="Number of unique sessions")
    top_pages: List[Dict[str, Any]] = Field(description="Top pages by views")
    top_events: List[Dict[str, Any]] = Field(description="Top custom events")
    hourly_stats: List[Dict[str, Any]] = Field(description="Hourly statistics")
    daily_stats: List[Dict[str, Any]] = Field(description="Daily statistics")


class RealtimeStatsResponse(BaseModel):
    """Schema for real-time statistics response"""
    active_sessions: int = Field(description="Number of active sessions")
    page_views_last_hour: int = Field(description="Page views in the last hour")
    top_pages_today: List[Dict[str, Any]] = Field(description="Top pages today")
    recent_events: List[TrackingEventResponse] = Field(description="Recent events")
