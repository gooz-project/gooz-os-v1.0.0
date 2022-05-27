from machine import freq
from wifuxlogger import WifuxLogger as LOG

def cpu_freq(cmds):
    try:
        current_freq = int(freq())/10**6
        changed_freq = int(cmds[1])*10**6
        message = LOG.info("Machine's frequency was changed from {}MHz to {}MHz".format(int(current_freq), int(cmds[1])))
        freq(int(changed_freq))
        return message
    except Exception as ex:
        return LOG.error(ex)
