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
		# copy systemd services
		# cp -RT system/ /etc/systemd/system
		:
	} && {
		# enable all services
		# for service in system/*.service; do
		# 	sudo systemctl enable $(basename $service)
		# done
		:
	} && {
		# copy wallpaper image
		cp -RT Pictures/ /home/pi/Pictures
	} && {
		echo "Installation was succesful!"
	}
} || {
	echo "Installation failed. You can still try the manual way, instructions can be found in the README file."
}
