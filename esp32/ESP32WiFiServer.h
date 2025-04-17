#ifndef ESP32WIFISERVER_H
#define ESP32WIFISERVER_H

#include <WiFi.h>

class ESP32WiFiServer {
  private:
    const char* ssid;      // Wi-Fi SSID
    const char* password;  // Wi-Fi Password
    uint16_t port;         // TCP Port
    WiFiServer server;     // TCP server object
    WiFiClient client;     // Connected client

  public:
    bool clientConnected;  // Client connection status
    // Constructor
    ESP32WiFiServer(const char* ssid, const char* password, uint16_t port)
      : ssid(ssid), password(password), port(port), server(port), clientConnected(false) {}

    // Initialize Wi-Fi Access Point
    bool begin() {

      if (!WiFi.softAP(ssid, password)) {
        Serial.println("Failed to start the Access Point.");
        return false;
      }

      IPAddress myIP = WiFi.softAPIP();
      Serial.print("Access Point created. IP address: ");
      Serial.println(myIP);

      server.begin();
      Serial.println("TCP server started. Waiting for clients...");
      return true;
    }

    // Check for new client connections
    void checkForClient() {
      client = server.available();  // Check for an incoming client
      if (client) {
        clientConnected = true;
        Serial.print("Client connected. IP: ");
        Serial.println(client.remoteIP());

        // Send initial message to the client
        client.println("Hello from ESP32!");
      }
    }

    void sendData(const String& data) {
      if (clientConnected && client.connected()) {
        client.print(data);
        Serial.print("Sent data: ");
        Serial.println(data);
      } else {
        if (clientConnected) {
          Serial.println("Client disconnected.");
          clientConnected = false;
        }
      }
    }

    String receiveCommand() {
      static String commandBuffer = "";  // Buffer to store partial command data

      if (clientConnected && client.connected()) {
        while (client.available()) {
          char receivedChar = client.read();  // Read one character at a time

          if (receivedChar == '\n') {
            // End of command
            String command = commandBuffer;  // Copy the buffer to a command variable
            commandBuffer = "";              // Clear the buffer for the next command
            command.trim();                  // Remove trailing whitespace or newline
            Serial.print("Received command: ");
            Serial.println(command);
            return command;                  // Return the complete command
          } else {
            commandBuffer += receivedChar;   // Append character to the buffer
          }
        }
      }

  return "";  // Return an empty string if no complete command is received
}

    String formatSensor(char type, int sensorId, int data) {
      return String(type) + String(sensorId) + "_" + String(data);
    }

    String formatReader(char type, const String& data) {
      return String(type) + "_" + data;
    }

  };


#endif
