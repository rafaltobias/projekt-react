"""
Base schemas for API responses and common DTOs
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = Field(description="Whether the operation was successful")
    message: Optional[str] = Field(default=None, description="Response message")


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")


class PaginatedResponse(BaseModel):
    """Base paginated response schema"""
    page: int = Field(description="Current page number")
    per_page: int = Field(description="Items per page")
    total: Optional[int] = Field(default=None, description="Total number of items")
    has_next: Optional[bool] = Field(default=None, description="Whether there are more pages")


class PaginationParams(BaseModel):
    """Pagination parameters schema"""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=50, ge=1, le=100, description="Items per page")


class DateRangeParams(BaseModel):
    """Date range parameters schema"""
    days: int = Field(default=30, ge=1, le=365, description="Number of days to include")
    start_date: Optional[datetime] = Field(default=None, description="Start date")
    end_date: Optional[datetime] = Field(default=None, description="End date")
