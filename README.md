# Telemetry Central Unit
Central unit for acquisition, communication and memorization of data coming from sensors mounted in different places of the sailboat.
Actual sensors:
- GPS
- Wind sensor

# Installation Instructions (Raspbian)
First of all, you need to install a daemon to communicate with the GPS module.
We use [gpsd](https://gpsd.gitlab.io/gpsd/index.html), it can be installed with the following line:
```
sudo apt-get install gpsd gpsd-clients
```
If you have problem with the installation of gpsd please refer [here](https://gpsd.gitlab.io/gpsd/installation.html).

The folder structure of this repos maps each folder to a folder on the Raspberry Pi following this pattern:
```
<pi-folder>/filename
```
Where `<pi-folder>` is the last folder of the file path.

To install the files in the appropiate folder copy the folders accordingly to the following scheme:

Repo Folder | R-Pi Folder
------------|------------
autostart/  | /home/pi/.config/autostart
bin/        | /home/pi/bin
default/    | /etc/default
system/     | /etc/systemd/system/
