"""
API routers for the ESP32 message server
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .schemas import (
    MessageCreate, 
    MessageResponse, 
    MessageListResponse,
    MessageStatsResponse,
    MessageDeleteResponse
)
from .crud import message_crud
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["messages"])


@router.post("/data", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new message from ESP32
    """
    try:
        db_message = message_crud.create_message(db, message_data)
        logger.info(f"Received message #{db_message.id}: '{message_data.message}'")
        
        return MessageResponse(
            id=db_message.id,
            message=db_message.message,
            client_timestamp=db_message.client_timestamp,
            server_timestamp=db_message.server_timestamp,
            source=db_message.source
        )
    except Exception as e:
        logger.error(f"Ошибка создания сообщения: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка обработки сообщения: {str(e)}"
        )


@router.get("/data", response_model=MessageListResponse)
def get_messages(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get all messages with pagination
    """
    try:
        messages = message_crud.get_messages(db, limit, offset)
        total_count = message_crud.get_total_count(db)
        
        return MessageListResponse(
            status="success",
            total_count=total_count,
            returned_count=len(messages),
            limit=limit,
            offset=offset,
            messages=[
                MessageResponse(
                    id=msg.id,
                    message=msg.message,
                    client_timestamp=msg.client_timestamp,
                    server_timestamp=msg.server_timestamp,
                    source=msg.source
                ) for msg in messages
            ]
        )
    except Exception as e:
        logger.error(f"Ошибка получения сообщений: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении сообщений"
        )


@router.get("/data/latest", response_model=MessageResponse)
def get_latest_message(db: Session = Depends(get_db)):
    """
    Get the latest message
    """
    try:
        message = message_crud.get_latest_message(db)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет сообщений"
            )
        
        return MessageResponse(
            id=message.id,
            message=message.message,
            client_timestamp=message.client_timestamp,
            server_timestamp=message.server_timestamp,
            source=message.source
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения последнего сообщения: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении последнего сообщения"
        )


@router.get("/data/{message_id}", response_model=MessageResponse)
def get_message_by_id(
    message_id: int,
    db: Session = Depends(get_db)
):
    """
    Get message by ID
    """
    try:
        message = message_crud.get_message_by_id(db, message_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сообщение с ID {message_id} не найдено"
            )
        
        return MessageResponse(
            id=message.id,
            message=message.message,
            client_timestamp=message.client_timestamp,
            server_timestamp=message.server_timestamp,
            source=message.source
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения сообщения {message_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении сообщения"
        )


@router.get("/stats", response_model=MessageStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    Get server statistics
    """
    try:
        stats = message_crud.get_stats(db)
        return MessageStatsResponse(
            status="success",
            statistics=stats
        )
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении статистики"
        )


@router.delete("/data", response_model=MessageDeleteResponse)
def clear_all_messages(db: Session = Depends(get_db)):
    """
    Clear all messages
    """
    try:
        count = message_crud.delete_all_messages(db)
        logger.info(f"Cleared {count} messages")
        
        return MessageDeleteResponse(
            status="success",
            message=f"Очищено {count} сообщений"
        )
    except Exception as e:
        logger.error(f"Ошибка очистки сообщений: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при очистке сообщений"
        )


@router.delete("/data/{message_id}", response_model=MessageDeleteResponse)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete message by ID
    """
    try:
        deleted_message = message_crud.delete_message(db, message_id)
        if not deleted_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сообщение с ID {message_id} не найдено"
            )
        
        logger.info(f"Deleted message #{message_id}: '{deleted_message.message}'")
        
        return MessageDeleteResponse(
            status="success",
            message=f"Сообщение #{message_id} удалено",
            deleted_message=MessageResponse(
                id=deleted_message.id,
                message=deleted_message.message,
                client_timestamp=deleted_message.client_timestamp,
                server_timestamp=deleted_message.server_timestamp,
                source=deleted_message.source
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления сообщения {message_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении сообщения"
        )


@router.get("/search")
def search_messages(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search messages by text content
    """
    try:
        messages = message_crud.search_messages(db, query, limit)
        
        return {
            "status": "success",
            "query": query,
            "found_count": len(messages),
            "returned_count": min(limit, len(messages)),
            "messages": [
                MessageResponse(
                    id=msg.id,
                    message=msg.message,
                    client_timestamp=msg.client_timestamp,
                    server_timestamp=msg.server_timestamp,
                    source=msg.source
                ) for msg in messages
            ]
        }
    except Exception as e:
        logger.error(f"Ошибка поиска сообщений: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при поиске сообщений"
        )
