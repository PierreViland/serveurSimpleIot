#!/bin/bash

###Resauration Mac Addresse
echo "Désactivation de $INTERFACE..."
sudo ip link set wlan0 down
sudo macchanger -p wlan0
macchanger -s wlan0
sudo ip link set wlan0 up
# Nom de l'interface réseau (à personnaliser)
INTERFACE="wlan0"


echo "Désactivation de $INTERFACE..."
ip link set $INTERFACE down

# Configuration en mode DHCP
echo "Configuration de $INTERFACE en mode DHCP..."
dhclient $INTERFACE

# Vérification de l'état de l'interface
if [ $? -eq 0 ]; then
  echo "L'interface $INTERFACE est maintenant configurée avec une adresse IP dynamique."
  ip addr show $INTERFACE
else
  echo "Échec de la configuration de $INTERFACE."
fi

sudo ip link set $INTERFACE up
