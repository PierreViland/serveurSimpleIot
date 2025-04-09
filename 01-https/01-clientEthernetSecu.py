import ssl
import http.client
import json
import time

# Configuration réseau
server_url = "192.168.1.13"  # Adresse IP du serveur
server_port = 443  # Port HTTPS

# Certificats et clé
ca_cert_path = "./CertKey/CA/CA_Cyber.crt"  # Chemin vers le certificat CA
client_cert_path = "./CertKey/client/clientIot.crt"  # Chemin vers le certificat client
client_key_path = "./CertKey/client/clientIot.key"  # Chemin vers la clé privée du client

# Fonction pour simuler la lecture de température
def read_temperature():
    import random
    return round(20 + random.random() * 10, 2)  # Température simulée entre 20 et 30°C

def main():
    # Création d'un contexte SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert_path)
    context.load_cert_chain(certfile=client_cert_path, keyfile=client_key_path)

    while True :
        # Connexion au serveur
        connection = http.client.HTTPSConnection(server_url, server_port, context=context)
        try:
            print("Connexion au serveur...")

            # Données à envoyer
            temperature = read_temperature()
            payload = {
                "id": "ESP32-001",
                "temperature": temperature
            }
            json_data = json.dumps(payload)

            # Configuration de la requête POST
            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(json_data))
            }
            connection.request("POST", "/data", body=json_data, headers=headers)

            # Lecture de la réponse
            response = connection.getresponse()
            print(f"Statut : {response.status} {response.reason}")
            print("Réponse du serveur :")
            print(response.read().decode())
            time.sleep(2)
        except Exception as e:
            print("Erreur :", e)
        finally:
            connection.close()

if __name__ == "__main__":
    main()
