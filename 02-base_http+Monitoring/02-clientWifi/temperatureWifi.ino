#include <WiFi.h>
#include <HTTPClient.h>

// Configuration réseau
const char* ssid = "___________"; //Nom du réseau 
const char* password = "________________r"; //mot de passe

// Adresse du serveur et port
const char* serverURL = "http://_____________";  // Adresse IP du serveur
const uint16_t serverPort = 80;                 // Port du serveur

// Identifiant unique de l'ESP32
const String deviceID = "________________";

void setup() {
  Serial.begin(115200);

  // Connexion au réseau Wi-Fi
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
    // Lecture de la température interne (ou d'un capteur externe)
    float temperature = temperatureRead();  // Remplacez par une lecture réelle de température

    // Création de l'objet HTTP
    HTTPClient http;
    String url = String(serverURL) + ":" + String(serverPort) + "/data";  // URL complète
    http.begin(url);

    // Définir l'en-tête Content-Type pour envoyer des données JSON
    http.addHeader("Content-Type", "application/json");

    // Création des données au format JSON
    String postData = "{\"id\":\"" + String(deviceID) + "\",\"temperature\":" + String(temperature) + "}";

    // Envoi de la requête POST
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur d'envoi : " + String(httpResponseCode));
    }

    http.end();  // Fin de la requête HTTP
  } else {
    Serial.println("Déconnecté du Wi-Fi, tentative de reconnexion...");
    WiFi.reconnect();
  }

  delay(5000);  // Envoi toutes les 5 secondes
}

