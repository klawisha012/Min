#include <Wire.h>


int redPin = 6;    
int greenPin = 5;  
int bluePin = 3;   


const unsigned long DOT_DURATION = 500;         



const int MAX_QUEUE_SIZE = 10;
String messageQueue[MAX_QUEUE_SIZE];
int queueSize = 0;
int currentIndex = 0;
bool isPlaying = false;
String currentMorseCode = "";
String currentOriginalMessage = "";


struct MorseEntry {
  char letter;
  const char* code;
};


MorseEntry morseAlphabet[] = {
  {'A',"12"}, {'B',"2111"}, {'C',"2121"}, {'D',"211"}, {'E',"1"},
  {'F',"1121"}, {'G',"221"}, {'H',"1111"}, {'I',"11"}, {'J',"1222"},
  {'K',"212"}, {'L',"1211"}, {'M',"22"}, {'N',"21"}, {'O',"222"},
  {'P',"1221"}, {'Q',"2212"}, {'R',"121"}, {'S',"111"}, {'T',"2"},
  {'U',"112"}, {'V',"1112"}, {'W',"122"}, {'X',"2112"}, {'Y',"2122"}, {'Z',"2211"},
  {' ', "2222"} 
};
const int morseSize = sizeof(morseAlphabet)/sizeof(morseAlphabet[0]);


String getMorseCode(char c) {
  for (int i=0; i<morseSize; i++) {
    if (morseAlphabet[i].letter == c) {
      return String(morseAlphabet[i].code);
    }
  }
  return "";
}


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


String textToMorseCode(String text) {
  String result = "";
  text.toUpperCase();

  Serial.println("=== Соответствие букв и кодов Морзе ===");

  
  result += "333"; 

  for(int i = 0; i < text.length(); i++){
    char c = text[i];
    String code = getMorseCode(c);
    if (code.length() > 0) {
      Serial.print(c); 
      Serial.print(" - "); 
      Serial.println(code);
      result += code;

      
      if(c != ' ' && i < text.length() - 1 && text[i+1] != ' ') {
        result += "3"; 
      }
    }
  }

  
  Serial.println("================================");
  return result;
}


void addToQueue(String message) {
  if (queueSize < MAX_QUEUE_SIZE) {
    messageQueue[queueSize] = message;
    queueSize++;
    Serial.print("Сообщение добавлено в очередь. В очереди: ");
    Serial.println(queueSize);
    
    
    if (!isPlaying) {
      startNextMessage();
    }
  } else {
    Serial.println("Очередь переполнена! Сообщение не добавлено.");
  }
}


void startNextMessage() {
  if (currentIndex < queueSize) {
    String message = messageQueue[currentIndex];
    currentOriginalMessage = message;
    currentMorseCode = textToMorseCode(message);
    isPlaying = true;
    
    Serial.print("Начинаем воспроизведение: ");
    Serial.println(message);
    Serial.print("Осталось в очереди: ");
    Serial.println(queueSize - currentIndex - 1);
  } else {
    
    if (currentOriginalMessage != "") {
      Serial.println("Очередь пуста. Повтор последнего сообщения...");
      isPlaying = true;
    } else {
      isPlaying = false;
      Serial.println("Нет сообщений для воспроизведения.");
    }
  }
}


void playMorseSequence() {
  if (currentMorseCode == "") return;
  
  for (int i = 0; i < currentMorseCode.length(); i++) {
    char symbol = currentMorseCode[i];
    int color = (symbol == ' ') ? 0 : (symbol - '0');
    
    if(color > 0) {
      setLEDColor(color);
      delay(DOT_DURATION);
      setLEDColor(0); // выключить
    }
    
    
    if (Serial.available() > 0) {
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
          Serial.print("Новое сообщение получено во время воспроизведения: ");
          Serial.println(cleanWord);
          addToQueue(cleanWord);
        }
      }
    }
  }
  
 
  currentIndex++;
  
  if (currentIndex < queueSize) {
    
    startNextMessage();
  } else if (queueSize > 0) {
    
    currentIndex = queueSize - 1;
    Serial.println("Повтор последнего сообщения...");
  } else {
    
    isPlaying = false;
    currentMorseCode = "";
    currentOriginalMessage = "";
  }
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
  Serial.println("Сообщения добавляются в очередь и воспроизводятся по порядку");
}

void loop() {
  
  if (Serial.available() > 0) {
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
        addToQueue(cleanWord);
      } else {
        Serial.println("Ошибка: введите только буквы A-Z и пробелы");
      }
    }
  }

  
  if (isPlaying && currentMorseCode != "") {
    playMorseSequence();
  } else if (queueSize > 0) {
    
    startNextMessage();
  }
}