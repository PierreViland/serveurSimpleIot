#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
String ssid = "cielCyber"; 
String password = "XXXX"; 
String serverURL = "http://192.168.1.10";  
const uint16_t serverPort = 80;                
String deviceID = "CapteurSalle";

void setup() {
  Serial.begin(115200);
  Serial.print("Connexion à ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté au réseau Wi-Fi !");
  Serial.print("Adresse IP de l'ESP32 : ");
  Serial.println(WiFi.localIP());

  String mac = WiFi.macAddress();
  Serial.println("Adresse MAC de l'ESP32 :");
  Serial.println(mac);
}
void loop() {
  if (WiFi.status() == WL_CONNECTED) {   
    float temperature = temperatureRead();     
    HTTPClient http;
    String url = String(serverURL) + ":" + String(serverPort) + "/data";  
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    StaticJsonDocument<200> doc;
    doc["id"] = deviceID;
    doc["temperature"] = temperature;
    String postData;
    serializeJson(doc, postData);
    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur d'envoi : " + String(httpResponseCode));
    }
    http.end();  
  } else {
    Serial.println("Déconnecté du Wi-Fi, tentative de reconnexion...");
    WiFi.reconnect();
  }
  delay(5000);  
}
