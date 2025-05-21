import ssl
import http.client
import json
import time
import random
from datetime import datetime

# Configuration réseau
server_url = "192.168.1.30"
server_port = 443
device_id = "deviceTestEthernet"

# Chemins vers les certificats
ca_cert_path = "./certificat/caIot.crt"
client_cert_path = "./certificat/clientIot.crt"
client_key_path = "./certificat/clientIot.key"

# Simulation de lecture de température
def read_temperature():
    return round(20 + random.random() * 10, 2)

# Analyse du certificat SSL
def afficher_certificat(cert):
    if not cert:
        print("Aucun certificat serveur reçu.")
        return

    print("\n===== Certificat du serveur =====")
    subject = dict(x[0] for x in cert.get('subject', []))
    issuer = dict(x[0] for x in cert.get('issuer', []))

    print(f"Sujet (CN): {subject.get('commonName')}")
    print(f"Émetteur : {issuer.get('commonName')}")
    print(f"Valide du {cert.get('notBefore')} au {cert.get('notAfter')}")
    print("=================================\n")

# Fonction principale
def main():
    # Création du contexte SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert_path)
    context.load_cert_chain(certfile=client_cert_path, keyfile=client_key_path)
    # Forcer l'utilisation exclusive de TLSv1.2 :
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2  # Limite la version à TLSv1.2 uniquement


    while True:
        try:
            connection = http.client.HTTPSConnection(server_url, server_port, context=context)
            
            # Établir la connexion SSL pour obtenir le certificat
            connection.connect()
            cert = connection.sock.getpeercert()
            afficher_certificat(cert)

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

