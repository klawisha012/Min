import serial
import requests
import time
import json
from datetime import datetime

# Глобальная переменная для serial соединения
ser = None

def simple_esp32_client(serial_port, server_url):
    """Клиент для получения только декодированных сообщений"""
    global ser
    
    try:
        # Подключаемся к serial порту
        ser = serial.Serial(serial_port, 9600, timeout=1)
        time.sleep(2)
        print(f"Подключено к {serial_port}")
        print("Ожидание декодированных сообщений...")
        
        while True:
            try:
                if ser.in_waiting > 0:
                    # Читаем строку
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    if line:
                        # Фильтруем только сообщения с декодированным текстом
                        if line.startswith("MESSAGE:"):
                            message = line.replace("MESSAGE:", "").strip()
                            print(f"📨 Получено сообщение: {message}")
                            
                            # Формируем данные для отправки
                            data = {
                                "message": message,
                                "timestamp": datetime.now().isoformat(),
                                "source": "esp32_color_sensor"
                            }
                            
                            # Отправляем на сервер
                            try:
                                response = requests.post(
                                    server_url,
                                    json=data,
                                    headers={'Content-Type': 'application/json'},
                                    timeout=5
                                )
                                if response.status_code == 200:
                                    print("✓ Сообщение отправлено на сервер")
                                else:
                                    print(f"✗ Ошибка отправки: {response.status_code}")
                            except Exception as e:
                                print(f"✗ Ошибка связи с сервером: {e}")
                        
                        # Также выводим статусные сообщения
                        elif line in ["READY", "ERROR"]:
                            print(f"Статус ESP32: {line}")
            
            except serial.SerialException as e:
                print(f"Ошибка Serial порта: {e}")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
            
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        close_serial()

def close_serial():
    """Функция для закрытия serial соединения"""
    global ser
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial соединение закрыто")
        ser = None

# Обработка завершения программы
import atexit
atexit.register(close_serial)

if __name__ == "__main__":
    try:
        simple_esp32_client(
            serial_port="COM12",
            server_url="http://localhost:7999/api/data"
        )
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    finally:
        close_serial()