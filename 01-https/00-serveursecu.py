from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
import time
import logging
import socket
import threading

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)

HOST = '0.0.0.0'
PORT = 443  # Port HTTPS standard

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        logger.info("Réception d'une requête POST de %s", self.client_address)

        try:
                client_cert = self.connection.getpeercert()
                if client_cert:
                     logger.info("Certificat client reçu :")
                     logger.info("Sujet : %s", client_cert.get('subject'))
                     logger.info("Émetteur : %s", client_cert.get('issuer')) 
                else:
                     logger.warning("Aucun certificat client présenté.")
        except Exception as e:
                logger.error("Impossible d'extraire le certificat client : %s", e)

        
        # Afficher les informations SSL (si disponibles)
        try:
            ssl_info = self.connection.cipher()
            logger.info("Détails du chiffrement SSL : %s", ssl_info)
        except Exception as e:
            logger.warning("Impossible d'obtenir les détails du chiffrement SSL : %s", e)

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            device_id = data.get('id', 'ID inconnu')
            temperature = data.get('temperature', 'Température inconnue')

            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{current_timestamp} - ID : {device_id}")
            print(f"Température : {temperature}°C")
            if temperature > 100:
                print("+++++++++++ALERTE CHALEUR+++++++++++")
            elif temperature < 5:
                print("+++++++++++ALERTE GRAND FROID+++++++++++")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "OK"}).encode('utf-8'))

        except json.JSONDecodeError:
            logger.error("Erreur de décodage JSON : %s", post_data)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
        except Exception as e:
            logger.error("Erreur lors du traitement de la requête POST de %s : %s", self.client_address, e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Erreur interne du serveur")

    def handle(self):
        try:
            logger.info("Tentative de connexion de %s", self.client_address)
            super().handle()
        except ssl.SSLError as e:
            logger.warning("Échec de connexion SSL de %s : %s", self.client_address, e)
        except ConnectionResetError as e:
            logger.warning("Connexion réinitialisée par le client %s : %s", self.client_address, e)
        except Exception as e:
            logger.error("Erreur inattendue avec %s : %s", self.client_address, e)

    def log_message(self, format, *args):
        return  # Pour garder la console propre

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), RequestHandler)

    try:
        # Configuration du contexte SSL
 # Forcer TLS 1.2 uniquement
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(certfile='./certificat/serverIot_30.crt',
                                    keyfile='./certificat/serverIot_30.key')
        ssl_context.load_verify_locations(cafile='./certificat/caIot.crt')
        ssl_context.verify_mode = ssl.CERT_REQUIRED
    
        logger.info("Serveur HTTPS (TLS 1.2) démarré sur %s:%d", HOST, PORT)


        # Remplacement de .serve_forever()
        while True:
            try:
                newsocket, fromaddr = server.socket.accept()
                logger.info("Connexion entrante de %s", fromaddr)

                try:
                    # Tentative de handshake SSL
                    connstream = ssl_context.wrap_socket(newsocket, server_side=True)
                    threading.Thread(target=server.process_request, args=(connstream, fromaddr)).start()

                except ssl.SSLError as ssl_err:
                    logger.warning(" Tentative rejetée avec certificat non valide depuis %s : %s", fromaddr, ssl_err)
                    newsocket.close()

                except Exception as e:
                    logger.error("Erreur lors du traitement de la connexion de %s : %s", fromaddr, e)
                    newsocket.close()

            except KeyboardInterrupt:
                break

            except Exception as e:
                logger.error("Erreur dans la boucle principale du serveur : %s", e)

    except ssl.SSLError as e:
        logger.error("Erreur SSL lors de l'initialisation : %s", e)
    except socket.error as e:
        logger.error("Erreur de socket : %s", e)
    except Exception as e:
        logger.critical("Erreur critique lors du démarrage : %s", e)
    finally:
        logger.info("Arrêt du serveur.")
        server.server_close()
