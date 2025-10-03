from fastapi import FastAPI, HTTPException
import uvicorn
import serial
from schemas import Message

app = FastAPI()

# Настройки последовательного порта (подберите под вашу Arduino)
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = 1

def send_to_arduino(data_bytes: bytes) -> bool:
    """Функция для отправки данных в последовательный порт"""
    try:
        with serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=TIMEOUT
        ) as ser:
            ser.write(data_bytes)
            print(f"Отправлено в Arduino: {data_bytes}")
            return True
    except Exception as e:
        print(f"Ошибка отправки: {str(e)}")
        return False

@app.post("/")
def DataToArduino(message: Message):
    # Преобразуем текст в байты
    print(message.text)
    data_bytes = message.text.encode('utf-8')
    
    # Отправляем в Arduino
    if send_to_arduino(data_bytes):
        return {
            "status": "success",
            "message": "Данные отправлены в Arduino",
            "original_text": message.text,
            "sent_bytes": list(data_bytes)
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Ошибка отправки данных в Arduino"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)