#!/bin/bash

status=$?

# support files
cp -RT opt/ /opt
status+=$?

# shell scripts
cp -RT bin/ /usr/local/bin
status+=$?

# autostart files
cp -RT autostart/ /etc/xdg/autostart
status+=$?

# gpsd settings
sudo cp -RT default/ /etc/default
status+=$?

# sytemd services
sudo cp -RT system/ /etc/systemd/system
status+=$?

# wallpaper image
sudo cp -RT Pictures/ /home/pi/Pictures
status+=$?

# enable all services
for service in system/*.service; do
	sudo systemctl enable $(basename $service)
done
status+=$?

# check if everything was good
[ $status -eq 0 ] && echo "Installation was successful!" || echo "Installation failed. You can still try the manual way, instructions can be found in the README file."
