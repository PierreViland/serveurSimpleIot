import http.client
import json
import time
import random

# Configuration réseau
server_url = "192.168.1.30"
server_port = 80  # HTTP standard
device_id = "deviceTestEthernet"

# Simulation de lecture de température
def read_temperature():
    return round(20 + random.random() * 10, 2)

# Fonction principale
def main():
    while True:
        try:
            connection = http.client.HTTPConnection(server_url, server_port)

            # Préparer et envoyer la requête
            temperature = read_temperature()
            payload = {
                "id": device_id,
                "temperature": temperature,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            json_data = json.dumps(payload)

            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(json_data))
            }

            connection.request("POST", "/", body=json_data, headers=headers)
            response = connection.getresponse()

            print(f"Statut : {response.status} {response.reason}")
            print("Réponse du serveur :", response.read().decode())
            connection.close()
            time.sleep(2)

        except Exception as e:
            print("Erreur :", e)
            try:
                connection.close()
            except:
                pass
            time.sleep(2)

if __name__ == "__main__":
    main()

