#!/bin/bash

# autostart files
cp -RT autostart/ /home/pi/.config/autostart

# shell scripts
cp -RT bin/ /home/pi/bin

# gpsd settings
sudo cp -RT default/ /etc/default

# sytemd services
sudo cp -RT system/ /etc/systemd/system

# wallpaper image
sudo cp -RT Pictures/ /home/pi/Pictures

# enable all services
for service in system/*.service; do
	sudo systemctl enable $(basename $service)
done
