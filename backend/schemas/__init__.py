"""
Schemas package initialization
"""
from .base_schemas import BaseResponse, ErrorResponse, PaginatedResponse, PaginationParams, DateRangeParams
from .tracking_schemas import (
    TrackingEventRequest, TrackingEventResponse, TrackingEventCreateResponse,
    TrackingEventsResponse, SessionDataResponse, SessionAnalyticsResponse,
    TrackingStatsResponse, RealtimeStatsResponse
)
from .visit_schemas import VisitRequest, VisitResponse, VisitCreateResponse
from .tag_schemas import TagRequest, TagResponse, TagCreateResponse, TagsListResponse
from .stats_schemas import VisitStatsResponse, ComprehensiveStatsResponse, RealtimeVisitStatsResponse

__all__ = [
    # Base schemas
    'BaseResponse',
    'ErrorResponse', 
    'PaginatedResponse',
    'PaginationParams',
    'DateRangeParams',
    
    # Tracking schemas
    'TrackingEventRequest',
    'TrackingEventResponse',
    'TrackingEventCreateResponse',
    'TrackingEventsResponse',
    'SessionDataResponse',
    'SessionAnalyticsResponse',
    'TrackingStatsResponse',
    'RealtimeStatsResponse',
    
    # Visit schemas
    'VisitRequest',
    'VisitResponse', 
    'VisitCreateResponse',
    
    # Tag schemas
    'TagRequest',
    'TagResponse',
    'TagCreateResponse',
    'TagsListResponse',
    
    # Stats schemas
    'VisitStatsResponse',
    'ComprehensiveStatsResponse',
    'RealtimeVisitStatsResponse',
]
