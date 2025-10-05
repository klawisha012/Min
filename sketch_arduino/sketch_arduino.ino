#include <Wire.h>

// Пины для подключения RGB-светодиода
int redPin = 6;    
int greenPin = 5;  
int bluePin = 3;   

// Константы
const unsigned long DOT_DURATION = 500;         
const unsigned long COLOR_STABILIZE_DELAY = 100; 
//const unsigned long BETWEEN_SYMBOLS_DELAY = 100; 

bool isPlayingMorse = false;

// ---------- Словарь Морзе ----------
struct MorseEntry {
  char letter;
  const char* code;
};

// Таблица соответствия A-Z и пробел
MorseEntry morseAlphabet[] = {
  {'A',"12"}, {'B',"2111"}, {'C',"2121"}, {'D',"211"}, {'E',"1"},
  {'F',"1121"}, {'G',"221"}, {'H',"1111"}, {'I',"11"}, {'J',"1222"},
  {'K',"212"}, {'L',"1211"}, {'M',"22"}, {'N',"21"}, {'O',"222"},
  {'P',"1221"}, {'Q',"2212"}, {'R',"121"}, {'S',"111"}, {'T',"2"},
  {'U',"112"}, {'V',"1112"}, {'W',"122"}, {'X',"2112"}, {'Y',"2122"}, {'Z',"2211"},
  {' ', "2222"} // пробел между словами
};
const int morseSize = sizeof(morseAlphabet)/sizeof(morseAlphabet[0]);

// Поиск кода по букве
String getMorseCode(char c) {
  for (int i=0; i<morseSize; i++) {
    if (morseAlphabet[i].letter == c) {
      return String(morseAlphabet[i].code);
    }
  }
  return "";
}

// Управление LED
void setLEDColor(int color) {
  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);

  switch(color) {
    case 1: digitalWrite(redPin, HIGH); break;   // Красный
    case 2: digitalWrite(bluePin, HIGH); break;  // Синий
    case 3: digitalWrite(greenPin, HIGH); break; // Зелёный (разделитель)
  }
}

// Преобразуем текст в код Морзе
String textToMorseCode(String text) {
  String result = "";
  text.toUpperCase();

  Serial.println("=== Соответствие букв и кодов Морзе ===");

  // Начало передачи (синхро-сигнал)
  result += "333"; // зелёный–зелёный–зелёный

  for(int i = 0; i < text.length(); i++){
    char c = text[i];
    String code = getMorseCode(c);
    if (code.length() > 0) {
      Serial.print(c); 
      Serial.print(" - "); 
      Serial.println(code);
      result += code;

      // добавляем разделитель между символами, кроме пробела
      if(c != ' ' && i < text.length() - 1 && text[i+1] != ' ') {
        result += "3"; // разделитель символов
      }
    }
  }
  // конец передачи (синхро-сигнал)
  result += "333"; // зелёный–зелёный–зелёный
  Serial.println("================================");
  return result;
}

// Воспроизведение Morse
void playMorseSequence(String morseSequence, String originalText) {
  Serial.print("Полный морзе-код: ");
  Serial.println(morseSequence);
  isPlayingMorse = true;

  Serial.println("Начало передачи...");
  
  for (int i = 0; i < morseSequence.length(); i++) {
    char symbol = morseSequence[i];
    int color = (symbol == ' ') ? 0 : (symbol - '0');
    
    Serial.print("Передаем: ");
    switch(color) {
      case 1: Serial.println("Красный (1)"); break;
      case 2: Serial.println("Синий (2)"); break;
      case 3: Serial.println("Зеленый (3)"); break;
      default: Serial.println("Выключено"); break;
    }
    
    if(color > 0) {
      setLEDColor(color);
      delay(DOT_DURATION);
      setLEDColor(0); // выключить
    }
    //delay(BETWEEN_SYMBOLS_DELAY); // пауза между символами
  }

  Serial.println("=== Передача завершена ===");
  Serial.print("Исходное сообщение: ");
  Serial.println(originalText);
  Serial.print("Переданный код: ");
  Serial.println(morseSequence);
  Serial.println("================================");
  Serial.println();
  Serial.println("Введите следующее слово:");
  
  isPlayingMorse = false;
}

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  Serial.begin(9600);
  while (!Serial) { ; }

  Serial.println();
  Serial.println("Передатчик Morse готов!");
  Serial.println("Введите слово для кодирования в Морзе:");
}

void loop() {
  if (!isPlayingMorse && Serial.available() > 0) {
    String inputWord = Serial.readString();
    inputWord.trim();
    
    while(Serial.available() > 0) {
      Serial.read();
    }
    
    if(inputWord.length() > 0){
      inputWord.toUpperCase();
      String cleanWord = "";
      for(int i = 0; i < inputWord.length(); i++) {
        char c = inputWord[i];
        if((c >= 'A' && c <= 'Z') || c == ' ') {
          cleanWord += c;
        }
      }
      
      if(cleanWord.length() > 0){
        Serial.print("Получено слово: ");
      
        Serial.println(cleanWord);
        String morseCode = textToMorseCode(cleanWord);
        playMorseSequence(morseCode, cleanWord);
      } else {
        Serial.println("Ошибка: введите только буквы A-Z и пробелы");
        Serial.println("Введите слово для кодирования в Морзе:");
      }
    }
  }
}