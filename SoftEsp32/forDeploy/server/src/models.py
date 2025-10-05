"""
Database models for the ESP32 message server
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class Message(Base):
    """
    Model for storing ESP32 messages
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    client_timestamp = Column(String, nullable=True)
    server_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    source = Column(String, default="esp32_color_sensor", nullable=False)
    
    def __repr__(self):
        return f"<Message(id={self.id}, message='{self.message[:50]}...', source='{self.source}')>"

