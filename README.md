## Serveur Maison

Serveur réalisé en Python en écoute sur le port 80 ou 443 (possibilité de modifier). Il attend l'envoi d'un JSON avec l'ID d'un appareil et la température.

## Installation

Clonez le repository avec la commande suivante :

```bash
git clone [https://github.com/PierreViland/serveurMaison.git](https://github.com/PierreViland/serveurSimpleIot.git)
cd serveurSimpleIot
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


Les données envoyées par le client Ethernet (et aussi Wifi) sont au format JSON: 
```bash
data = {
    "id": device_id,
    "temperature": temperature
}
```

Il sera nécessaire d'installer des package python. Il est recommandé d'installer les packages dans des environnements virtuels. Ils permettent de segmenter les projets avec des versions spécifiques de Python et des des bibliothèques installées uniquement pour le projet.
our créer un environnement virtuel avec venv, on fait :

python -m venv <nom+nom_environnement_virtuel>

Et pour activer un environnement virtuel sur Windows Mac, les OS bases sur UNIX :

#### Sur Windows :
```bash
source cheim+nom_environnement_virtuel\Scripts\activate
```
#### Sur Linux :
```bash
source chemin+nom_environnement_virtuel/activate
```
Les packets à installer pour le client : 
```bash
pip install scapy  #Util pour l'usurpation
pip install requests
```

Le lancement du serveur s'effectue très simplement : 
```bash
sudo python3 00-serveurHttp.py 
```

Pour le client : 
```bash
python3 01-clientEthernet.py 
```


