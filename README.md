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
+ 02-recupertionTemperature : code pour un client wifi sur esp32 (.ino) mais obfusqué
+ 03-temperatureWifi_obfuscation
   + obfuscationCode.py : code permettant d'effectuer de l'obfuscation sur le code temperatureWifi_ex.ino. intéressant pour ne pas donner le mot de passe directmeent aux éleves. (Ils peuvent aussi s'amuser à trouver le mot de passe). 
   + temperatureWifi_ex.ino : code source du client .ino origine qui doit être obfusqué. Possibilité de s'en servir directement. 
+ 04-falsificationTrame
   + 00-changementAddr.sh : script permettant de remplacerl'adresse IP et l'adresse MAC d'une machine linux (testé avec kali). Il permet de prendre les adresses d'un device (code ci-dessus)
   + 01-hackerDevice_II.py : programme permettant permettant la deconnexion du device reél puis l'envoi de données erronées
   + 02-remiseAddr.sh : script permettant la remise en état du système 

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
#### Programme .ino
Les programmes .ino ont été testés (compilation et téléversement) avec IDE arduino avec ajout de la carte esp32 par espressif systems. 
Ils permettent de créer un objet connecté envoyant la température (réelle de la puce). 

## Utilisation de HTTPS
Le principe est le même mais il y a une authentification mutuelle et un chiffrement entre le client et le serveur. 
Il faut donc ajouter pour le serveur et le client : 
- sa clef privée
- son certificat signé par une CA
- Le certificat du CA
#### .ino
Dans la version sécurisé du client esp32, il est nécessaire d'installer la librairie esp32ping (pour vérifier que le client esp32 peut communiquer avec le serveur). Elle est disponible 

   + [ESP32Ping sur GitHub](https://github.com/marian-craciunescu/ESP32Ping)
Sinon, il est aussi possible de décommenter les lignes relatives aux ping.


** Remarque ** deux branches existent permettant d'imposer respectivement au serveur et au client l'utilisation du Tls V1.2
