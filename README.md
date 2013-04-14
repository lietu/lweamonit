# What is lweamonit

This is a collection of tools to make a little weather monitoring station, if you are
armed with a webcam, arduino, an extra server, and some sensors to your arduino.

Everything in this project is licensed under GPLv3 unless otherwise specified. See the LICENSE file, or at http://www.gnu.org/licenses/gpl-3.0.html .

I think at least the following have their own licenses:
 - image-generator/fonts/*
 - streamer/streamer_config.sh
 - arduino/OneWire.*
 - arduino/ds18b20p.*

 The DS18B20P library for Arduino is by me and with Creative Commons Attribution-ShareAlike 3.0 Unported 
 License., however when using lweamonit as a whole, you don't need to attribute me for that library. Only if
 you extract that library and do something else with it.


# Requirements

These are the requirements I am aware of:
- Arduino and a DS18B20-PAR sensor or some programming skill
- Linux / http://distrowatch.com/
- UVC driver compatible camera / http://www.ideasonboard.org/uvc/
- MJPG-streamer / http://sourceforge.net/projects/mjpg-streamer/
- Python / http://www.python.org/
- Bash / http://www.gnu.org/s/bash/

You could use some other OS and type of camera if you figure out how to get images off 
them yourself, other than mjpg_streamer. Please, feel free to modify the system to 
work with other OSes and camera types. I just wish you don't break any existing 
functionality, and contribute your patches to the project.

It shouldn't be that big of a PITA to support any other OS as long as you can set up a HTTP server to send the data or modify the image reader to fetch it otherwise. If you do, please do send me patches.


# How to set up lweamonit?

## You will need to set up your Arduino to send some temperature data.

In the arduino subfolder there is a project that I personally use for this.
It will function perfectly fine with a single DS18B20-PAR sensor. Open up the 
config.h -file and make sure the settings look ok. Then just deploy the code
on your Arduino with the Arduino IDE or any other tools you want to use.

If you do any custom coding the format expected by Python is as follows:
SENSOR_NAME1: 123.123|SENSOR_NAME2: 321.321

So pipe separated line with sensor name and numeric value separated with a colon.


## Set up the webcam server

If you have an UVC driver compatible camera (and the drivers installed), as well as
MJPG-streamer installed, you can use the tools in the streamer -subfolder to help
you run the image server.

Copy config.ini.template to config.ini and check that the values look good and then
add check_mjpg_streamer.sh to your crontab.


## Set up image generator

In the image-generator -subfolder is a Python application I've written to read data
off the USB port on linux, fetch an image the webcam server and draw the temperature
data on the image.

To use it, copy the config.json.template to config.json and configure to taste.

For more DejaVu fonts go to http://dejavu-fonts.org/ .

The software was written with purpose to support multiple different sensors drawn on
the image but that support wasn't finished because I got fed up with calculating the
pixels as it is. Maybe later.


## Set up publishing of your generated images

The easy way is to just have lweamonit image-generator to generate the images in your
public HTML folder or similar. However, if you're not planning on hosting the images
on the same server as you're running lweamonit on (like me), you should be able to
set up an rsync over SSH fairly easily to the server of your choosing.

For more information, go to http://bit.ly/158bNR5 .


# Where can I find more information?

If this documentation is not enough, you might find something more at 
http://github.com/lietu/lweamonit/ .
