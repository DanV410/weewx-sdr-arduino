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
