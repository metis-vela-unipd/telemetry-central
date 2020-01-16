#!/bin/bash

# Autostart folder
cp -RT autostart/ /home/pi/.config/autostart

# shell scripts
cp -RT bin/ /home/pi/bin

# gpsd settings
sudo cp -RT default/ /etc/default

# sytemd services
sudo cp -RT system/ /etc/systemd/system

# enable all services
for service in system/*.service; do
	sudo systemctl enable $(basename $service)
done
