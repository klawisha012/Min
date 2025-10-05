from fastapi import FastAPI, HTTPException
import uvicorn
import serial
from schemas import Message
from fastapi.middleware.cors import CORSMiddleware

DEBUG = True
app = FastAPI()

SERIAL_PORT = 'COM10'
BAUD_RATE = 9600
TIMEOUT = 1

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальный объект Serial
arduino_ser = None

@app.on_event("startup")
def startup_event():
    global arduino_ser
    try:
        arduino_ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        if DEBUG:
            print(f"Connected to Arduino on {SERIAL_PORT}")
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")

@app.on_event("shutdown")
def shutdown_event():
    global arduino_ser
    if arduino_ser and arduino_ser.is_open:
        arduino_ser.close()
        if DEBUG:
            print("Arduino port closed")

def send_to_arduino(text: str) -> bool:
    """Send text directly to Arduino"""
    global arduino_ser
    if not arduino_ser or not arduino_ser.is_open:
        print("Serial port is not open")
        return False
    try:
        # Отправляем текст с переводом строки для удобства Arduino
        arduino_ser.write((text + '\n').encode('utf-8'))
        if DEBUG:
            print(f"Sent to Arduino: {text}")
        return True
    except Exception as e:
        print(f"Send error: {str(e)}")
        return False

@app.post("/")
def DataToArduino(message: Message):
    if DEBUG:
        print(f"Text: {message.text}")
    if send_to_arduino(message.text):
        # Вычисляем количество байт в тексте
        text_bytes = len(message.text.encode('utf-8'))
        return {
            "status": "success",
            "message": "Text sent to Arduino",
            "original_text": message.text,
            "sent_bytes": message.text.encode('utf-8'),
            "bytes_count": text_bytes
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send data to Arduino"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
