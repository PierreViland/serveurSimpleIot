#!/bin/bash

# Variables
INTERFACE="wlan0"         # Interface Wi-Fi
NEW_IP="192.168.1.71"     # Nouvelle adresse IP
NETMASK="255.255.255.0"   # Masque de sous-réseau
GATEWAY="192.168.1.1"     # Passerelle par défaut
MACDEVICE="C8:C9:A3:FC:B1:DC" # Adresse MAC cible

# Diagnostic initial
echo "État initial de l'interface réseau :"
ip addr show $INTERFACE

# Modifier l'adresse MAC
echo "Modification de l'adresse MAC pour $INTERFACE..."
sudo ip link set $INTERFACE down
sudo macchanger -m $MACDEVICE $INTERFACE
macchanger -s $INTERFACE

# Réactiver l'interface
echo "Activation de l'interface..."
sudo ip link set $INTERFACE up


# Configuration IP statique
echo "Configuration IP statique..."
sudo ip addr flush dev $INTERFACE
sudo ip addr add $NEW_IP/24 dev $INTERFACE

# Configurer la passerelle par défaut
echo "Configuration de la passerelle..."
sudo ip route add default via $GATEWAY dev $INTERFACE

# Vérification finale
echo "Diagnostic après configuration :"
ip addr show $INTERFACE

echo "Configuration terminée."
