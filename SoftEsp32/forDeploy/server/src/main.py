from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import uvicorn

from .database import engine, Base
from .routers import router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('esp32_server.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация базы данных при запуске
def init_database():
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")


# Создание приложения FastAPI
app = FastAPI(
    title="ESP32 Message Server",
    description="Сервер для приема и хранения сообщений от ESP32 с поддержкой базы данных",
    version="2.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:80",
        "http://127.0.0.1:80",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Подключаем роутеры
app.include_router(router)


@app.on_event("startup")
def on_startup():
    """Вызывается при запуске приложения"""
    logger.info("Server starting...")
    init_database()


@app.on_event("shutdown")
def on_shutdown():
    """Вызывается при остановке приложения"""
    logger.info("Server stopping...")
    engine.dispose()


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "ESP32 Message Server",
        "status": "running",
        "version": "2.0.0",
        "description": "Сервер с поддержкой базы данных",
        "endpoints": {
            "send_message": "POST /api/data",
            "get_messages": "GET /api/data",
            "get_latest": "GET /api/data/latest",
            "get_by_id": "GET /api/data/{id}",
            "get_stats": "GET /api/stats",
            "search": "GET /api/search",
            "clear_all": "DELETE /api/data",
            "delete_by_id": "DELETE /api/data/{id}",
            "health": "GET /health",
        },
    }


@app.get("/health")
def health_check():
    """Проверка здоровья сервера"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "ESP32 Message Server v2.0.0",
        "database": "connected",
    }


@app.options("/{path:path}")
def options_handler(path: str):
    """Ответ на OPTIONS-запросы (CORS preflight)"""
    return {"message": "CORS preflight"}


def main():
    """Запуск сервера"""
    print("=" * 50)
    print("ESP32 Message Server v2.0.0")
    print("Logs saved to esp32_server.log")
    print("Server available at http://localhost:7999")
    print("CORS configured for localhost:5173 and localhost:3000")
    print("Database: PostgreSQL or SQLite")
    print("=" * 50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7999,
        log_level="info"
    )


if __name__ == "__main__":
    main()
