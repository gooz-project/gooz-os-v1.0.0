from esp32 import raw_temperature, hall_sensor
from wifuxlogger import WifuxLogger as LOG


def cpu_temperature(cmds):
    tf = raw_temperature()
    if '-f' in cmds:
        if '-n' in cmds:
            return "{:4.2f}".format(tf)
        return LOG.info("{:4.2f} degree Fahrenheit".format(tf))
    tc = (tf-32.0)/1.8
    if '-n' in cmds:
        return "{:4.1f}".format(tc)
    return LOG.info("{:4.1f} degree Celcius".format(tc))


def hall(cmds):
    if '-n' in cmds:
        return hall_sensor()
    return LOG.info(hall_sensor())
