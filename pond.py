#!/usr/bin/python
#
# Portions Copyright 2014 Matthew Wall
# Portions taken from the pond.py example on the "add sensor" page on the weewx wiki, edited by Tom Keffer
#
# weewx service that reads data from a file as key value pairs and adds it to every loop packet
#
# This driver will read data from a file.  Each line of the file is a 
# name=value pair, for example:
#
# inTemp=50
# pressure=1009.4
# inHumidity=75
#
# The names must match the weewx database schema, but the schema can be extended for new fields
#
# The units must be in the weewx.US unit system:
#   degree_F, inHg, inch, inch_per_hour, mile_per_hour
#
# Add this service to weewx.conf, then restart weewx 
#[Engine]
#[[Services]]
#    data_services = ..., user.pond.PondService
#
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# See http://www.gnu.org/licenses/

import syslog
import weewx
from weewx.wxengine import StdService

class PondService(StdService):
    def __init__(self, engine, config_dict):
        super(PondService, self).__init__(engine, config_dict)      
        d = config_dict.get('PondService', {})
        self.filename = d.get('filename', '/var/www/html/data/reading.txt')
        syslog.syslog(syslog.LOG_INFO, "pond: using %s" % self.filename)
        self.bind(weewx.NEW_LOOP_PACKET, self.read_file)

    def read_file(self, event):
        data= {}
        try:
            with open(self.filename) as f:
		for line in f:
                    eq_index = line.find('=')
                    name = line[:eq_index].strip()
                    value = line[eq_index + 1:].strip()
                    data[name] = value
        except Exception, e:
            logerr("read failed: %s" % e)
        for vname in data:
            event.packet[vname] = float(data[vname])
