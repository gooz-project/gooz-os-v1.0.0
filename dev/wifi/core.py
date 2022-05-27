from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
import network
sta_if = network.WLAN(network.STA_IF)

def run(cmds):
    return eval("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def connect(cmds):
    blueprint = EngineTemplate.parameter_parser(cmds)
    if not sta_if.isconnected():
        LOG.debug('connecting to network...')
        try:
            sta_if.active(True)
            sta_if.connect(blueprint["--name"], blueprint["--password"])
        except Exception as ex:
            return LOG.error(ex)
    return LOG.info('Connection Successfull')

def disconnect(cmds):
    sta_if.active(False)
    sta_if.active(True)
    return LOG.debug(sta_if.isconnected())

def ifconfig(cmds):
    info = sta_if.ifconfig()
    message = ""
    if sta_if.isconnected():
        message = "<BROADCASTING>"
    else:
        message = "<>"
    
    return LOG.info("""
--------------------------
Network Information
--------------------------
{}
--------------------------
Access Point Name: str(sta_if.config('essid'))
Access Point MAC Address: str(sta_if.config('mac'))
--------------------------
Your Device IP: {}
Subnet Mask: {}
Gateway: {}
DNS: {}""".format(message,info[0],info[1],info[2],info[3])) 
    

def ls(cmds):
    wlans = sta_if.scan()
    message = "\n"
    for i in wlans:
        message += str(i[0])+"\n"
    return LOG.debug("Available WLANs")+message


def on(cmds):
    sta_if.active(True)
    return LOG.info("WiFi ON")


def off(cmds):
    sta_if.active(False)
    return LOG.info("WiFi OFF")

def status(cmds):
    status_code = sta_if.status()
    if status_code == 1000:
        return LOG.info("No Connection and No Activities")
    elif status_code == 1001:
        return LOG.info("Connecting")
    elif status_code == 202:
        return LOG.error("Failed due to password error")
    elif status_code == 201:
        return LOG.warning("Failed, because there is no access point reply")
    elif status_code == 1010:
        return LOG.info("Connected")
    elif status_code == 203:
        return LOG.error("Failed")
    elif status_code == 200:
        return LOG.error("Timeout")
    elif status_code == 204:
        return LOG.error("Handshake timeout")
    
