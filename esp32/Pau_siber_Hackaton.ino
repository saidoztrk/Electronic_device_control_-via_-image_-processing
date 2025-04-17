#include "ESP32WiFiServer.h"
#include "RGB_COLORS.h"
#include "CuteBuzzerSounds.h"

//Buzzer
#define BUZZER_PIN 2

// WIFI PARAMETRELERI
const char *ssid = "esp32siber";
const char *password = "pausiber24";
bool server_status;
String heartbeat = "HEARTBEAT";
unsigned long previousMillis = 0;
const long heartbeat_interval = 1000;

uint32_t chipId = 0;

// WIFI BAGLANTISI
ESP32WiFiServer wifiServer(ssid, password, 2024);

void setup() {

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  cute.init(BUZZER_PIN);


  Serial.begin(115200);
  delay(2000);
  Serial.println("MCU-STARTUP..");
}

void loop() {
  //WIFI BAGLANTILARININ KONTROL EDILECEGI KISIM
  if (!server_status)
  {
    blue();
    server_status = wifiServer.begin();
  }
  else if (!wifiServer.clientConnected)
  {
    red();
    wifiServer.checkForClient();
    green();
  }

  if (wifiServer.clientConnected) {
    
    String command = wifiServer.receiveCommand();
    if (!command.isEmpty())
    {
      magenta();
      if (command == "TURN_ON")
      {
        white();
        Serial.println("LED1 turned ON.");
      }
      else if (command == "TURN_OFF") 
      {
        white();
        Serial.println("LED1 turned OFF.");
      }
      else if (command == "MOTOR_START") 
      {
        white();
        Serial.println("Motor started.");
      }
      else if (command == "MOTOR_STOP") 
      {
        white();
        Serial.println("Motor stopped.");
      } 
      else if (command == "MAGENTA") 
      {
        magenta();
        Serial.println("Led to MAGENTA");
      }
      else if (command == "CYAN") 
      {
        cyan();
        Serial.println("Led to CYAN");
      } 
      else if (command == "ORANGE") 
      {
        orange();
        Serial.println("Led to ORANGE");
      }
      else if (command == "RED") 
      {
        red();
        Serial.println("Led to RED");
      } 
      else if (command == "GREEN") 
      {
        green();
        Serial.println("Led to GREEN");
      }
      else if (command == "BLUE") 
      {
        blue();
        Serial.println("Led to BLUE");
      }
      else if (command == "BUZZER1") 
      {
        cute.play(S_CONNECTION);
        Serial.println("Buzzer1");
      }
      else if (command == "BUZZER2") 
      {
        cute.play(S_DISCONNECTION);
        Serial.println("Buzzer2");
      }
      else if (command == "GETCHIP_ID") 
      {
        String data = "";
        data += "\nESP32 Chip model = " + String(ESP.getChipModel()) + " Rev " + String(ESP.getChipRevision()) + " ";
        data += "This chip has " + String(ESP.getChipCores()) + " cores ";
        data += "Chip ID: " + String(chipId) + "\n";
        wifiServer.sendData(data);
      }
      else if (command == "EMPTY") 
      {
        blue();
        Serial.println("Led to BLUE");
      }
      else if (command == "EMPTY")
      {
        blue();
        Serial.println("Led to BLUE");
      }

      else
      {
        off();
        Serial.println("Unknown command.");
      }
    }

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= heartbeat_interval) 
    {
      previousMillis = currentMillis;
      wifiServer.sendData(heartbeat);
    }
  }
}