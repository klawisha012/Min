import serial
import time
from config import SERIAL_PORT, BAUD_RATE

class SerialHandler:
    def __init__(self):
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            print(f"Подключено к {SERIAL_PORT}")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_text(self, text):
        if self.ser and self.ser.is_open:
            self.ser.write((text + '\n').encode())

    def read_line(self):
        if self.ser and self.ser.is_open and self.ser.in_waiting > 0:
            return self.ser.readline().decode().strip()
        return None