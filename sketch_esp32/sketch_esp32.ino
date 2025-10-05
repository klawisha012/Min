#include <Wire.h>
#include "Adafruit_TCS34725.h"

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

// Калибровочные коэффициенты
float redCorrection = 0.85;
float greenCorrection = 1.1;  
float blueCorrection = 0.95;

String colorSequence = "";
String PrevText = "";
unsigned long lastReadTime = 0;
const unsigned long READ_INTERVAL = 500;

bool isRecording = false;
int greenCount = 0;

String decodeMorseSequence(String seq) {
    String morseAlphabet[26] = {
    "12","2111","2121","211","1","1121","221","1111","11","1222",
    "212","1211","22","21","222","1221","2212","121","111","2",
    "112","1112","122","2112","2122","2211"
   };

   String decodedText = "";
   String tempLetter = "";

   // Разбиваем по "2222" (пробел между словами)
   int lastPos = 0;
   while (true) {
      int nextPos = seq.indexOf("2222", lastPos);
     String wordPart = (nextPos == -1) ? seq.substring(lastPos) : seq.substring(lastPos, nextPos);

      // Разбиваем это слово на буквы по разделителю '3'
      tempLetter = "";
      for (int i = 0; i < wordPart.length(); i++) {
        char c = wordPart[i];

        if (c == '3') {
          if (tempLetter.length() > 0) {
            bool found = false;
           for (int j = 0; j < 26; j++) {
              if (tempLetter == morseAlphabet[j]) {
               decodedText += (char)('A' + j);
                found = true;
               break;
             }
            }
            if (!found) decodedText += '?';
            tempLetter = "";
          }
        } else {
          tempLetter += c;
        }
     }

      if (tempLetter.length() > 0) {
        bool found = false;
        for (int j = 0; j < 26; j++) {
          if (tempLetter == morseAlphabet[j]) {
            decodedText += (char)('A' + j);
            found = true;
            break;
          }
        }
      if (!found) decodedText += '?';
        tempLetter = "";
    }

    if (nextPos == -1) 
      break;
    decodedText += ' ';
    lastPos = nextPos + 4;
    }

  return decodedText;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  if (tcs.begin()) {
    Serial.println("READY");
  } else {
    Serial.println("ERROR");
    while (1);
  }
  
  lastReadTime = millis();
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastReadTime >= READ_INTERVAL) {
    uint16_t red, green, blue, clear;
    tcs.getRawData(&red, &green, &blue, &clear);
    
    // Применяем калибровку
    uint16_t correctedRed = red * redCorrection;
    uint16_t correctedGreen = green * greenCorrection; 
    uint16_t correctedBlue = blue * blueCorrection;
    
    // Определяем цвет после коррекции
    char currentColor = '0';
    
    if (correctedRed > correctedGreen && correctedRed > correctedBlue) {
      currentColor = '1';
    }
    else if (correctedGreen > correctedRed && correctedGreen > correctedBlue) {
      currentColor = '3';
    }
    else if (correctedBlue > correctedRed && correctedBlue > correctedGreen) {
      currentColor = '2';
    }
    else {
      currentColor = '0';
    }
    
    if (!isRecording) {
      // Режим ожидания старта
      if (currentColor == '3') {
        greenCount++;
      } else {
        greenCount = 0;
      }
      
      if (greenCount >= 3) {
        isRecording = true;
        colorSequence = "";
        greenCount = 0;
      }
    } else {
      // Режим записи
      if (currentColor == '3') {
        greenCount++;
      } else {
        greenCount = 0;
      }
      
      colorSequence += currentColor;
      
      // Проверяем окончание записи
      if (greenCount >= 3) {
        // Декодируем сообщение
        String decodedMessage = decodeMorseSequence(colorSequence);
        
        // Отправляем ТОЛЬКО декодированное сообщение
        Serial.print("MESSAGE:");
        Serial.println(decodedMessage);
        
        PrevText = decodedMessage;
        colorSequence = "";
      }
    }
    
    lastReadTime = currentTime;
  }
}