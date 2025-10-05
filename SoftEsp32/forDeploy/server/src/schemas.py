"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    """Base message schema"""
    message: str
    timestamp: Optional[str] = None
    source: Optional[str] = "esp32_color_sensor"


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessageResponse(MessageBase):
    """Schema for message response"""
    id: int
    client_timestamp: Optional[str] = None
    server_timestamp: datetime
    source: str

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """Schema for message list response"""
    status: str
    total_count: int
    returned_count: int
    limit: int
    offset: int
    messages: List[MessageResponse]


class MessageStatsResponse(BaseModel):
    """Schema for statistics response"""
    status: str
    statistics: dict


class MessageDeleteResponse(BaseModel):
    """Schema for delete response"""
    status: str
    message: str
    deleted_message: Optional[MessageResponse] = None

