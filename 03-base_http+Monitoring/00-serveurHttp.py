from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
from prometheus_client import start_http_server, Counter, Histogram, Gauge


# Configuration du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 80        # Port d'écoute

PROMETHEUS_PORT = 8800  # Port pour exposer les métriques Prometheus

# Démarrer le serveur Prometheus pour exposer les métriques
def start_prometheus_server():
    start_http_server(PROMETHEUS_PORT)
    print(f"Serveur Prometheus en écoute sur le port {PROMETHEUS_PORT}...")


# Créer un compteur pour les requêtes POST
post_requests_counter = Counter('http_post_nb_requete', 'Nombre total de requete POST')

response_time_histogram = Histogram(
    'http_temps_reponse', 
    'Histogramme des temps de réponse HTTP (s)',
    buckets=[0.001, 0.0015, 0.002, 0.003, 0.005, 0.0075]  # Définir les buckets pour l'histogramme
)
# Variable globale pour stocker l'heure de la dernière requête
last_request_time = None

# Créer une métrique pour le temps écoulé entre les requêtes
time_between_requests_gauge = Gauge('http_time_between_requests_seconds', 'Temps entre chaque requête en secondes')



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global last_request_time
	# Longueur des données reçues
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        #Enregistrer le temps de début
        start_time = time.time()
        
        if last_request_time is not None:
            time_elapsed = start_time - last_request_time
            time_between_requests_gauge.set(time_elapsed)  # Mettre à jour la métrique
            print(f"Temps écoulé depuis la dernière requête : {time_elapsed:.2f} secondes")
        else:
            print("Première requête reçue, pas de temps écoulé calculé.")
        # Mettre à jour l'heure de la dernière requête
        last_request_time = start_time
        
        # Incrémenter le compteur de requêtes POST
        post_requests_counter.inc()
        
        # Longueur des données reçues
        print(f"Nombre total de requêtes POST reçues : {post_requests_counter._value.get()}")


        # Traitement des données JSON
        try:
            data = json.loads(post_data)
            device_id = data.get('id', 'ID inconnu')
            temperature = data.get('temperature', 'Température inconnue')

            # Affichage des données
            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{current_timestamp}ID : {device_id}")
            print(f"Température : {temperature}°C")
            if temperature > 100 : 
                print("+++++++++++ALERTE CHALEUR+++++++++++")
            elif temperature < 5 : 
                print("+++++++++++ALERTE GRAND FROID+++++++++++")

            # Réponse au client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "OK"}).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")

    def log_message(self, format, *args):
        return  

# Lancer le serveur
if __name__ == "__main__":
    start_prometheus_server()  # Demarre le serveur Prometheus
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Serveur en écoute sur le port {PORT}...")
    try:
        server.serve_forever()  # Le serveur écoute en continu
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
        server.server_close()  # Ferme proprement le serveur
        print("Serveur arrêté.")
