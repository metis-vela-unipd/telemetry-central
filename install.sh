#!/bin/bash

# console colors
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

{
	{
		# copy support files
		cp -RT opt/ /opt
	} && {
		# copy shell scritps
		cp -RT bin/ /usr/local/bin
	} && {
		# copy autostart files
		cp -RT autostart/ /etc/xdg/autostart
	} && {
		# copy gpsd settings
		cp -RT default/ /etc/default
	} && {
		# copy nginx settings
		cp -RT nginx/ /etc/nginx
	} && {
		# remove default site symlink
		rm -f /etc/nginx/sites-enabled/default
		# create custom site symlink
		ln -sf /etc/nginx/sites-available/telemetry /etc/nginx/sites-enabled
	} &&{
		# copy systemd services
		cp -RT system/ /etc/systemd/system
	} && {
		# enable all services
		for service in system/*.service; do
			systemctl enable $(basename $service)
		done
	} && {
		# copy wallpaper image
		cp -RT Pictures/ /home/pi/Pictures
	} && {
		echo -e "${GREEN}Installation was succesful!${RESET}\n"
	}
} || {
	echo -e "${RED}Installation failed. You can still try the manual way, instructions can be found in the README file.${RESET}\n"
}
