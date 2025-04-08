from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

# Configuration du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 80         # Port d'écoute

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Longueur des données reçues
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

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
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Serveur en écoute sur le port {PORT}...")
    try:
        server.serve_forever()  # Le serveur écoute en continu
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
        server.server_close()  # Ferme proprement le serveur
        print("Serveur arrêté.")
