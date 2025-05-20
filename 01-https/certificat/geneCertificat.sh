#!/bin/bash

# Définition des fichiers
CA_KEY="caIot.key"   # Clé privée du CA
CA_CERT="caIot.crt"  # Certificat du CA

SERVER_KEY="serverIot_30.key"
SERVER_CSR="serverIot_30.csr"
SERVER_CERT="serverIot_30.crt"
SERVER_EXT="serverIot_30.ext"

# Partie Client
CLIENT_KEY="clientIot.key"
CLIENT_CSR="clientIot.csr"
CLIENT_CERT="clientIot.crt"
CLIENT_EXT="clientIot.ext"

# Common Name
CA_CN="CA_Broce"
SERVER_CN="serv_Iot.com"
IP_SERVER="192.168.1.30"
CLIENT_CN="clientIot"

# Création du CA (décommentez si nécessaire)
# echo "Création de la clé privée de la CA..."
openssl genrsa -out $CA_KEY 2048
# echo "Création du certificat auto-signé de la CA..."
openssl req -x509 -new -key $CA_KEY -sha256 -days 3650 -out $CA_CERT -subj "/CN=$CA_CN"

# --------------------
# Partie Serveur
# --------------------
echo "Création de la clé privée du serveur..."
openssl genrsa -out $SERVER_KEY 2048

echo "Création de la demande de certificat du serveur..."
openssl req -new -key $SERVER_KEY -out $SERVER_CSR -subj "/CN=$SERVER_CN"

cat > $SERVER_EXT <<EOF
[ v3_ext ]
subjectAltName = IP:$IP_SERVER
EOF

echo "Signature du certificat serveur avec la CA..."
openssl x509 -req -in $SERVER_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $SERVER_CERT -days 365 -sha256 -extfile $SERVER_EXT -extensions v3_ext

echo "Certificat serveur généré :"
openssl x509 -in $SERVER_CERT -text -noout

# --------------------
# Partie Client
# --------------------
echo "Création de la clé privée du client..."
openssl genrsa -out $CLIENT_KEY 2048

echo "Création de la demande de certificat du client..."
openssl req -new -key $CLIENT_KEY -out $CLIENT_CSR -subj "/CN=$CLIENT_CN"

cat > $CLIENT_EXT <<EOF
[ v3_ext ]
extendedKeyUsage = clientAuth
EOF

echo "Signature du certificat client avec la CA..."
openssl x509 -req -in $CLIENT_CSR -CA $CA_CERT -CAkey $CA_KEY -out $CLIENT_CERT -days 365 -sha256 -extfile $CLIENT_EXT -extensions v3_ext

echo "Certificat client généré :"
openssl x509 -in $CLIENT_CERT -text -noout

