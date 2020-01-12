#!/bin/bash

# Autostart folder
cp -RT autostart/ /home/pi/.config/autostart

# shell scripts
cp -RT bin/ /home/pi/bin

# gpsd settings
sudo cp -RT default/ /etc/default
