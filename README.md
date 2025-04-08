## Serveur Maison

Serveur réalisé en Python en écoute sur le port 80. Il attend l'envoi d'un JSON avec l'ID d'un appareil et la température.

## Installation

Clonez le repository avec la commande suivante :

```bash
git clone https://github.com/PierreViland/serveurMaison.git
cd serveurMaison
```

## Utilisation de HTTP (non sécurisé)

Pour faire des échanges en HTTP, 
```bash
cd 00-base_http
```

Ce repertoire contient : 
+ 00-serveurHTTP.Py : serveur en python 
+ 01-clientEthernet.py : client en python
+ 02-clientWifi : code pour un client wifi sur esp32


Les données envoyées sont : 
'''bash
data = {
    "id": device_id,
    "temperature": temperature
}
'''
