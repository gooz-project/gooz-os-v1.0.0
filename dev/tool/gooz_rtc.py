from machine import RTC
from wifuxlogger import WifuxLogger as LOG
from ntptime import settime
from engine.engine_template import EngineTemplate as GoozEngine

class RTCErrors():
    @staticmethod
    def no_wifi_error():
        return LOG.error("Please check your wifi connection!\n")+LOG.error("try: wifi status ") 
    
def run(cmds):
    if not len(cmds)>1:
        return LOG.error("Please enter a command!\n")+LOG.info("Use 'rtc help' for help")
    elif cmds[1][0] == "_":
        return "ERROR"
    return eval("{}({})".format(cmds[1],cmds))

def help(cmds):
    commands=['set','autoset','show']
    message = ""
    for command in commands:
        message += command + "\n"
    return "Commands: \n"+message+"\n0: Year, 1: Month, 2: Day of Month, 3: Day of week\n4: Hour, 5: Minute, 6: Second, 7: Milisecond"

def set(cmds):
    m_rtc = RTC()
    #dates_tuple = m_rtc.datetime()
    dates= []
    blueprint = {}
    blueprint = GoozEngine.parameter_parser(cmds, blueprint)
    for i in range(0,8):
        if f'--{i}' in blueprint.keys():
            dates.append(int(blueprint[f'--{i}']))
        else:
            dates.append(m_rtc.datetime()[i])
    m_rtc.datetime(dates)
    return LOG.debug("RTC date had configured as {}".format(str(dates)))
    
def autoset(cmds):
    message = ""
    try:
        settime()
        m_rtc = RTC()
        message = LOG.debug(m_rtc.datetime())
        del m_rtc
    except Exception as ex:
        message = LOG.error("Error while getting current date! ")
        if str(ex) == "[Errno 118] EHOSTUNREACH" or str(ex) == "-202":
            message += "\n"+RTCErrors.no_wifi_error()
        else:
            message += "\n"+LOG.error(str(ex))
    return message

def show(cmds):
    m_rtc = RTC()
    return m_rtc.datetime()

