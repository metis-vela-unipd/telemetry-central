#!/bin/bash

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
		# create console logs directory
		mkdir -p /var/log/telemetry
		# grant write permissions to user 'pi'
		chown pi: /var/log/telemetry
	} && {
		# copy wallpaper image
		cp -RT Pictures/ /home/pi/Pictures
	} && {
		echo -e "Installation was succesful!"
	}
} || {
	echo -e "Installation failed. You can still try the manual way, instructions can be found in the README file."
}
