String oeird32(String obf, int shift = 3) {
  String res = "";
  for (int i = 0; i < obf.length(); i++) {
    char c = obf.charAt(i);
    if (c >= 32 && c <= 126) {
      c = (c - 32 - shift + 95) % 95 + 32;
    }
    res += c;
  }
  return res;
}

String _obf_0 = oeird32("flhoF|ehu");
String _obf_1 = oeird32("urfnvwdu");
String _obf_2 = oeird32("kwws=224<5149;14143");
String _obf_3 = oeird32("FdswhxuVdooh");
String _obf_4 = oeird32("Frqqh{lrq#à#");
String _obf_5 = oeird32("1");
String _obf_6 = oeird32("_qFrqqhfwé#dx#uévhdx#Zl0Il#$");
String _obf_7 = oeird32("Dguhvvh#LS#gh#o*HVS65#=#");
String _obf_8 = oeird32("Dguhvvh#PDF#gh#o*HVS65#=");
String _obf_9 = oeird32("=");
String _obf_10 = oeird32("2gdwd");
String _obf_11 = oeird32("Frqwhqw0W|sh");
String _obf_12 = oeird32("dssolfdwlrq2mvrq");
String _obf_13 = oeird32("lg");
String _obf_14 = oeird32("whpshudwxuh");
String _obf_15 = oeird32("Uésrqvh#gx#vhuyhxu#=#");
String _obf_16 = oeird32("Huuhxu#g*hqyrl#=#");
String _obf_17 = oeird32("Géfrqqhfwé#gx#Zl0Il/#whqwdwlyh#gh#uhfrqqh{lrq111");

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
String ssid = _obf_0; 
String password = _obf_1; 
String serverURL = _obf_2;  
const uint16_t serverPort = 80;                
String deviceID = _obf_3;

void setup() {
  Serial.begin(115200);
  Serial.print(_obf_4);
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(_obf_5);
  }
  Serial.println(_obf_6);
  Serial.print(_obf_7);
  Serial.println(WiFi.localIP());

  String mac = WiFi.macAddress();
  Serial.println(_obf_8);
  Serial.println(mac);
}
void loop() {
  if (WiFi.status() == WL_CONNECTED) {   
    float temperature = temperatureRead();     
    HTTPClient http;
    String url = String(serverURL) + _obf_9 + String(serverPort) + _obf_10;  
    http.begin(url);
    http.addHeader(_obf_11, _obf_12);
    StaticJsonDocument<200> doc;
    doc[_obf_13] = deviceID;
    doc[_obf_14] = temperature;
    String postData;
    serializeJson(doc, postData);
    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(_obf_15 + response);
    } else {
      Serial.println(_obf_16 + String(httpResponseCode));
    }
    http.end();  
  } else {
    Serial.println(_obf_17);
    WiFi.reconnect();
  }
  delay(5000);  
}
