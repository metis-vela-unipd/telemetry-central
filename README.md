# Telemetry for Raspberry Pi
Central unit for acquisition, communication and memorization of data coming from sensors mounted in different places of the sailboat.
Actual sensors:
- GPS
- Wind sensor

# Installation Instructions (Raspbian)
### Using the installer
Simply run the `install.sh` script in the root folder of the repository:
```
sudo bash install.sh
```

### The manual way
If the installer method doesn't work it's still possible to try with the manual way. The folder structure of this repos maps each folder to a folder on the Raspberry Pi following this pattern:
```
<pi-folder>/filename
```
Where `<pi-folder>` is the last folder of the file path.

To install the files in the appropiate folder copy the folders accordingly to the following scheme:

Repo Folder | R-Pi Folder
------------|------------
opt/        | /opt
bin/        | /usr/local/bin
autostart/  | /etc/xdg/autostart
default/    | /etc/default
nginx/      | /etc/nginx
system/     | /etc/systemd/system
Pictures/   | /home/pi/Pictures

Then enable all the services in the `/system` folder by doing:
```
sudo systemctl enable <service-name>
```
Where `<service-name>` is the name of the file without the extension (e.g. file name: `jupyter.service` -> service name: `jupyter`).

Finally enable the telemetry webapp:
```
sudo ln -s /etc/nginx/sites-available/telemetry /etc/nginx/sites-enabled
```
 