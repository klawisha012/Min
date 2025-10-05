"""
Database CRUD operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from .models import Message
from .schemas import MessageCreate


class MessageCRUD:
    """CRUD operations for Message model"""
    
    @staticmethod
    def create_message(db: Session, message_data: MessageCreate) -> Message:
        """Create a new message"""
        db_message = Message(
            message=message_data.message,
            client_timestamp=message_data.timestamp,
            source=message_data.source
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        result = db.execute(select(Message).where(Message.id == message_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    def get_messages(
        db: Session, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Message]:
        """Get messages with pagination"""
        result = db.execute(
            select(Message)
            .order_by(Message.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    def get_latest_message(db: Session) -> Optional[Message]:
        """Get the latest message"""
        result = db.execute(
            select(Message)
            .order_by(Message.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    def get_total_count(db: Session) -> int:
        """Get total count of messages"""
        result = db.execute(select(func.count(Message.id)))
        return result.scalar()
    
    @staticmethod
    def search_messages(
        db: Session, 
        query: str, 
        limit: int = 20
    ) -> List[Message]:
        """Search messages by text content"""
        result = db.execute(
            select(Message)
            .where(Message.message.ilike(f"%{query}%"))
            .order_by(Message.id.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    def delete_message(db: Session, message_id: int) -> Optional[Message]:
        """Delete message by ID"""
        message = MessageCRUD.get_message_by_id(db, message_id)
        if message:
            db.delete(message)
            db.commit()
        return message
    
    @staticmethod
    def delete_all_messages(db: Session) -> int:
        """Delete all messages and return count"""
        result = db.execute(select(func.count(Message.id)))
        count = result.scalar()
        
        db.execute(delete(Message))
        db.commit()
        return count
    
    @staticmethod
    def get_stats(db: Session) -> dict:
        """Get statistics about messages"""
        total_count = MessageCRUD.get_total_count(db)
        
        # Get first and last message timestamps
        first_result = db.execute(
            select(Message.server_timestamp)
            .order_by(Message.id.asc())
            .limit(1)
        )
        first_timestamp = first_result.scalar_one_or_none()
        
        last_result = db.execute(
            select(Message.server_timestamp)
            .order_by(Message.id.desc())
            .limit(1)
        )
        last_timestamp = last_result.scalar_one_or_none()
        
        return {
            "total_messages": total_count,
            "first_message_time": first_timestamp.isoformat() if first_timestamp else None,
            "last_message_time": last_timestamp.isoformat() if last_timestamp else None,
            "server_uptime": "running"
        }


# Create instance for easy import
message_crud = MessageCRUD()

