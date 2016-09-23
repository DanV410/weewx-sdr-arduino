# weewx-sdr-arduino
Sketch, PHP, and Weewx service to use SDR Driver and this service to replace Acurite console

Parts you need:

BME280 - Pressure Temperature Humidity sensor. I used the DiyMall breakout board available on Amazon for $10.
HiLetgo New Version NodeMCU LUA WiFi Internet ESP8266 Development - $9 on Amazon
NooElec NESDR Nano 2 - Tiny Black RTL-SDR USB Set (RTL2832U + R820T2) $20 on Amazon
Micro USB cable and phone charger - You probably have an extra at this point
Solderless breadboard and jumper wires - $6 on Amazon if you don't already have one

Architecture:

Load Arduino firmware onto the NodeMCU. I followed the directions here:

http://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/

Grab these librarys and install them:

https://github.com/DaKaZ/esp8266-restclient
https://github.com/adafruit/Adafruit_BME280_Library

Load the reading.ico sketch onto your board ( i need to upload this)

This sketch connects to a wifi access point, and then makes GET calls to a web server running PHP. The URL is calls contains the readings in a key=value format. The temperature (inTemp) is in Farenheit, the pressure (pressure) in millibars, and the humidity (inHumidity) in %RH.

The test.php file on your web server takes the content of the GET request and saves it to a file named reading.txt in the data subdirectory. 

The pond.py service reads the key-value pairs and appends them to every loop packet. I cobbled this together mostly by borrowing parts of pond.py and fileparse.py and combining them to do what I needed. I don't have a pond, but was too lazy to change the name. I also don't know python all that well, so I'm sure there are some poor programming practices used.

One thing to note is that the pond.py service passes along the value as US units, so a entry is needed in the calibrations section of weewx.conf to convert this to C for the loop packet. I use 

inTemp = (inTemp-32)/1.8

I'm going to be adding a solar/UV sensor, probably connected to a second NodeMCU, and will have pond.py read a second file form the web server.

It's not pretty, but it works. I'll probably make it more robust and handle errors better. I also need to add the comments back in to include copyrights and gnu license stuff.

Thanks to Ton Keffer and Matt Wall for all their work on weewx.
