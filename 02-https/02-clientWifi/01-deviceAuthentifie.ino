
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP32Ping.h>

// Configuration réseau 
const char* ssid = "...........";
const char* password = "...........";
const char* serverURL = ".............";  // Adresse IP du serveur
const uint16_t serverPort = 443;         // Port HTTPS



// Certificats
const char* ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
......................
......................
-----END CERTIFICATE-----
)EOF";

const char* client_cert = R"EOF(
-----BEGIN CERTIFICATE-----
......................
......................
-----END CERTIFICATE-----
)EOF";

const char* client_key = R"EOF(
-----BEGIN PRIVATE KEY-----
......................
......................
-----END PRIVATE KEY-----
)EOF";

void setup() {
  Serial.begin(115200);

  // Connexion Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnecté au réseau Wi-Fi !");
  Serial.print("Adresse IP de l'ESP32 : ");
  Serial.println(WiFi.localIP());


//Test pour voir si on peut communiquer avec le serveur
  bool success = Ping.ping("...........", 3);
 
  if(!success){
    Serial.println("Ping failed");
    return;
	} 
  Serial.println("Ping succesful.");

	
}

void loop() {
  WiFiClientSecure client;
  client.setCACert(ca_cert);
  client.setCertificate(client_cert);
  client.setPrivateKey(client_key);
  

  if (client.connect(serverURL, serverPort)) {
    Serial.println("\nConnecté au réseau !");
    Serial.print("Adresse IP de l'ESP32 : ");
    Serial.println(WiFi.localIP());

    float temperature = temperatureRead();
    String postData = "{\"id\":\"ESP32-____\",\"temperature\":" + String(temperature) + "}";
 
    client.println("POST /data HTTP/1.1");
    client.println("Host: " + String(serverURL));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.print(postData);

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") break;
    }

    String response = client.readString();
    Serial.println("Réponse du serveur : " + response);
  } else {
    Serial.println("Erreur de connexion au serveur !");
  }

  client.stop();
  delay(2000);
}