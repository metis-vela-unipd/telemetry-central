#!/bin/bash

{
	{
		# Copy support files
		cp -RT opt/ /opt
	} && {
		# Copy shell scritps
		cp -RT bin/ /usr/local/bin
	} && {
		# Copy autostart files
		cp -RT autostart/ /etc/xdg/autostart
	} && {
		# Copy gpsd settings
		cp -RT default/ /etc/default
	} && {
		# Copy nginx settings
		cp -RT nginx/ /etc/nginx
	} && {
		# Remove default site symlink
		rm -f /etc/nginx/sites-enabled/default
		# Create custom site symlink
		ln -sf /etc/nginx/sites-available/telemetry /etc/nginx/sites-enabled
	} &&{
		# Copy systemd services
		cp -RT system/ /etc/systemd/system
	} && {
		# Enable all services
		for service in system/*.service; do
			systemctl enable $(basename $service)
		done
	} && {
		# Create console logs directory
		mkdir -p /var/log/telemetry
		# Grant write permissions to user 'pi'
		chown pi: /var/log/telemetry
	} && {
		# Copy wallpaper image
		cp -RT Pictures/ /home/pi/Pictures
	} && {
		echo -e "Installation was succesful!"
	}
} || {
	echo -e "Installation failed. You can still try the manual way, instructions can be found in the README file."
}
