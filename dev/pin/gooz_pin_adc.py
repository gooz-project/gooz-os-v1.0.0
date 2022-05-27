from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
from machine import ADC, Pin, RTC
from dev.pin.core import CommonCommands
from dev.tool.gooz_thread import _gooz_start_function_thread


class Usage():
    @staticmethod
    def var_usage():
        return LOG.info('Usage -> pin var adc --name [PIN_NAME] --pin [PIN_NUMBER]')

    @staticmethod
    def delete_usage():
        return LOG.info('Usage -> pin adc delete [PIN_NAME]')+'\n'+LOG.info('deletes registered adc pin named [PIN_NAME]')+'\n'+LOG.info('To delete all registered adc pins -> pin adc delete all')

    @staticmethod
    def update_usage():
        return LOG.info('Usage -> pin adc update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]')+'\n'+LOG.info('updates the [VALUE_TO_CHANGE] value of the adc pin named [PIN_NAME] to [NEW_VALUE]')

    @staticmethod
    def show_usage():
        return LOG.info('Usage -> pin adc show')+'\n'+LOG.info('shows all registered adc pins')+'\n'+LOG.info('Usage -> pin adc show [PARAMETER]:[VALUE_TO_SEARCH_FOR]')+'\n'+LOG.info('shows specific adc pins')

    @staticmethod
    def read_usage():
        return LOG.info('Usage -> pin adc read [PIN_NAME] [READ_COUNT]')+'\n'+LOG.info('reads value [READ_COUNT] times.If not entered, reads once')

    @staticmethod
    def listen_usage():
        message = ""
        message += LOG.info('Usage -> pin adc listen [PIN_NAME]')+'\n'
        message += LOG.info('reads value from adc pin named [PIN_NAME] every 1 second')+'\n'
        message += LOG.info('Usage -> pin adc listen [PIN_NAME] --file [FILE_NAME] --date [DATE_BOOL] --loop [LOOP_COUNT] --delay [SLEEP_TIME] --end [END_CHARACTER]')+'\n'
        message += LOG.info('If [FILE_NAME] entered, the readed value will be written in the given [FILE_NAME]')+'\n'
        message += LOG.info('[DATE_BOOL] can be 1 or 0.Default value is 1.')+'\n'
        message += LOG.info('If [LOOP_COUNT] is bigger than 0, the number of reads will be the given number.Default [LOOP_COUNT] is -1 that means, it will read until stopped manually.')
        return message


def help(cmds):
    message = ""
    command_list = ['var', 'delete', 'update', 'show', 'read', 'listen']
    if not len(cmds) > 3:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> pin adc help [COMMAND]')
    try:
        return eval('Usage.{}_usage()'.format(cmds[3]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[3]))


def delete(cmds):
    return CommonCommands(cmds).delete()        


def registry(cmds):
    blueprint = {"pinType": "adc", "--name": "", "--pin": ""}
    return CommonCommands(cmds).register(blueprint)


def update(cmds):
    return CommonCommands(cmds).update()


def show(cmds):
    return CommonCommands(cmds).show()


def run(cmds):
    if not len(cmds) > 2:
        return LOG.warning("Please enter command!\n")+help(cmds)
    if cmds[2][0] == '_':
        return "ERROR"
    return eval("{}({})".format(cmds[2], EngineTemplate.exec_formatter_api(cmds)))


def read(cmds):
    message = ""
    pin = CommonCommands(cmds).get_pin(cmds[1], cmds[3])
    #blueprint = EngineTemplate.parameter_parser(cmds)
    try:
        runner_pin = ADC(Pin(int(pin["--pin"])))
        runner_pin.atten(ADC.ATTN_11DB)
        reading = runner_pin.read()
        del runner_pin
        if '-n' in cmds:
            return reading
        else:
            return LOG.info(reading)
    except Exception as ex:
        return LOG.error(ex)


def listen(cmds):
    if not len(cmds) > 3:
        return LOG.error("Please enter pin name!")
    blueprint = {"--delay": "1", "--file": "", "--end": "\n", "--loop": "-1"}# -d : date
    listen_conf = EngineTemplate.parameter_parser(cmds, blueprint)
    thread_conf = {'delay': listen_conf['--delay'], 'loop': listen_conf['--loop'], 'type': 'adc_listen', 'pin_name': cmds[3]}
    del blueprint
    pin = CommonCommands(cmds).get_pin(cmds[1], cmds[3])
    try:
        _gooz_start_function_thread(_adc_listen_thread, (pin, listen_conf), thread_conf)
        del listen_conf
        return "The pin is listened"
    except Exception as ex:
        del listen_conf
        return LOG.error(ex)


def _adc_listen_thread(pins, conf={}):
    message = ""
    try:
        runner_pin = ADC(Pin(int(pins["--pin"])))
        runner_pin.atten(ADC.ATTN_11DB)
        if conf["--file"] == "":
            print('Value of the ADC pin named "{}": '.format(pins["--name"]) + str(runner_pin.read()))
        else:
            if '-d' in conf.keys():
                m_rtc = RTC()
                f = open(conf["--file"], "a")
                f.write("{} {}{}".format(runner_pin.read(), m_rtc.datetime(), conf["--end"]))
                f.close()
            else:
                f = open(conf["--file"], "a")
                f.write("{}{}".format(runner_pin.read(), conf["--end"]))
                f.close()
    except Exception as ex:
        return LOG.error(ex)
