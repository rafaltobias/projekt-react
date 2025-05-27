"""
Statistics related DTOs and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class VisitStatsResponse(BaseModel):
    """Schema for visit statistics response"""
    total_visits: int = Field(description="Total number of visits")
    unique_visitors: int = Field(description="Number of unique visitors")
    page_views: int = Field(description="Total page views")
    bounce_rate: float = Field(description="Bounce rate percentage")
    average_session_duration: Optional[float] = Field(default=None, description="Average session duration")
    top_pages: List[Dict[str, Any]] = Field(description="Top pages by visits")
    top_referrers: List[Dict[str, Any]] = Field(description="Top referrers")
    countries: List[Dict[str, Any]] = Field(description="Visits by country")
    browsers: List[Dict[str, Any]] = Field(description="Visits by browser")
    operating_systems: List[Dict[str, Any]] = Field(description="Visits by OS")
    devices: List[Dict[str, Any]] = Field(description="Visits by device")
    hourly_visits: List[Dict[str, Any]] = Field(description="Hourly visit distribution")
    daily_visits: List[Dict[str, Any]] = Field(description="Daily visit distribution")


class ComprehensiveStatsResponse(BaseModel):
    """Schema for comprehensive statistics response"""
    overview: Dict[str, Any] = Field(description="Overview statistics")
    time_series: Dict[str, Any] = Field(description="Time series data")
    geographic: Dict[str, Any] = Field(description="Geographic data")
    technology: Dict[str, Any] = Field(description="Technology data")
    behavior: Dict[str, Any] = Field(description="User behavior data")
    performance: Dict[str, Any] = Field(description="Performance metrics")


class RealtimeVisitStatsResponse(BaseModel):
    """Schema for real-time visit statistics response"""
    active_visitors: int = Field(description="Number of active visitors")
    visits_last_hour: int = Field(description="Visits in the last hour")
    visits_today: int = Field(description="Visits today")
    top_pages_now: List[Dict[str, Any]] = Field(description="Top pages right now")
    recent_visits: List[Dict[str, Any]] = Field(description="Recent visits")
    live_events: List[Dict[str, Any]] = Field(description="Live events stream")
