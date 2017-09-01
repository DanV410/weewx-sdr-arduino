#!/usr/bin/python
#
# Portions Copyright 2014 Matthew Wall
# Portions taken from the pond.py example on the "add sensor" page on the weewx wiki, edited by Tom Keffer
#
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

from __future__ import with_statement
import syslog
import time
import paho.mqtt.client as mqtt
import weewx
from weewx.wxengine import StdService

class PondService(StdService):
    def __init__(self, engine, config_dict):
        super(PondService, self).__init__(engine, config_dict)      
        self.bind(weewx.NEW_LOOP_PACKET, self.on_message)

        self.host = config_dict.get('host', 'localhost')
        # subscribe to all sub-topic of the topic define in weewx.conf 
        self.topic = config_dict.get('topic', 'sensor') + "/#"

      	self.clientid = config_dict.get('client', 'weewx_mqttc')
        # how often to poll the weather data file, seconds
        self.poll_interval = float(config_dict.get('poll_interval', 5.0))
        # mapping from variable names to weewx names
        self.label_map = config_dict.get('label_map', {})

    loginf("host is %s" % self.host)
    loginf("topic is %s" % self.topic)
    loginf("polling interval is %s" % self.poll_interval)
    loginf('label map is %s' % self.label_map)
    self.client = mqtt.Client(client_id=self.clientid, protocol=mqtt.MQTTv31)
    self.client.on_message = self.on_message
    
    def logmsg(dst, msg):
        syslog.syslog(dst, 'pond: %s' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)

    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)

    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)
    
	

	self.client.connect(self.host, 1883, 60)
	self.client.subscribe(self.topic, qos=0)

  # The callback for when a PUBLISH message is received from the server.
  def on_message(self, client, userdata, msg):
  	  data= {}
      self.payload = str(msg.payload)
	    string_topic = str(msg.topic)
	    key =  string_topic.split('/')[-1] 
      data[key] = str(msg.payload)
      for vname in data:
            event.packet[vname] = float(data[vname])
            
  def closePort(self):
	    self.client.loop_stop()
      self.client.disconnect()




