#include <Wire.h>
#include "Adafruit_TCS34725.h"

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

// Калибровочные коэффициенты
float redCorrection = 0.85;
float greenCorrection = 1.1;  
float blueCorrection = 0.95;

int redPin = 13;    
int greenPin = 12;  
int bluePin = 14;   

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

   
   int lastPos = 0;
   while (true) {
      int nextPos = seq.indexOf("2222", lastPos);
     String wordPart = (nextPos == -1) ? seq.substring(lastPos) : seq.substring(lastPos, nextPos);

      
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

void setRGBColor(int color) {
  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);

  switch(color) {
    case 1: digitalWrite(redPin, HIGH); break;   
    case 2: digitalWrite(bluePin, HIGH); break; 
    case 3: digitalWrite(greenPin, HIGH); break;
    default: break; 
  }
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  
  setRGBColor(0);

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
    
    
    uint16_t correctedRed = red * redCorrection;
    uint16_t correctedGreen = green * greenCorrection; 
    uint16_t correctedBlue = blue * blueCorrection;
    
   
    char currentColor = '0';
    int detectedColor = 0;
    
    if (correctedRed > correctedGreen && correctedRed > correctedBlue) {
      currentColor = '1';
      detectedColor = 1; 
    }
    else if (correctedGreen > correctedRed && correctedGreen > correctedBlue) {
      currentColor = '3';
      detectedColor = 3; 
    }
    else if (correctedBlue > correctedRed && correctedBlue > correctedGreen) {
      currentColor = '2';
      detectedColor = 2; 
    else {
      currentColor = '0';
      detectedColor = 0; 
    }

    setRGBColor(detectedColor);
    
    if (!isRecording) {
      
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
      
      if (currentColor == '3') {
        greenCount++;
      } else {
        greenCount = 0;
      }
      
      colorSequence += currentColor;
      
      
      if (greenCount >= 3) {
        
        String decodedMessage = decodeMorseSequence(colorSequence);
        
        
        Serial.print("MESSAGE:");
        Serial.println(decodedMessage);
        
        PrevText = decodedMessage;
        colorSequence = "";
      }
    }
    
    lastReadTime = currentTime;
  }
}
