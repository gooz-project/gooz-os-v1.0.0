from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
import ujson
import utime
from machine import Pin, SoftI2C
from dev.tool.gooz_thread import _gooz_start_function_thread
from etc.config.core import _find_value
from dev.pin.core import CommonCommands


class Usage():
    @staticmethod
    def var_usage():
        return LOG.info('Usage -> pin var i2c --name "pin_name" --scl "scl_pin" --sda "sda_pin" --baud "frequency(MHz)" --address "address"')

    @staticmethod
    def delete_usage():
        return LOG.info('Usage -> pin i2c delete "pin_name"')+'\n'+LOG.info('pin i2c delete "pin_name" command deletes registered i2c pins by pin_name')+'\n'+LOG.info('To delete all registered i2c pins -> pin i2c delete all')

    @staticmethod
    def update_usage():
        return LOG.info('Usage -> pin i2c update "pin_name"')+'\n'+LOG.info('pin i2c update command updates registered i2c pins by pin_name')

    @staticmethod
    def show_usage():
        message = ""
        message += LOG.info('Usage -> pin i2c show') + '\n'
        message += LOG.info('shows all registered i2c pins') + '\n'
        message += LOG.info('Usage -> pin i2c show [PARAMETER]:[VALUE_TO_SEARCH_FOR]') + '\n'
        message += LOG.info('shows specific i2c pins')
        return message

    @staticmethod
    def write_usage():
        return LOG.info('Usage -> pin i2c write [PIN_NAME] --data [TX_DATA]')+'\n'+LOG.info('sends [TX_DATA] message to [PIN_NAME]')

    @staticmethod
    def read_usage():
        return LOG.info('Usage -> pin i2c read [PIN_NAME] --byte [BYTE_SIZE]')+'\n'+LOG.info('takes message from [PIN_NAME] in lenght [BYTE_SIZE]')

    @staticmethod
    def listen_usage():
        return LOG.info('Usage -> pin i2c listen [PIN_NAME]')+'\n'+LOG.info('takes message from [PIN_NAME] continuously in thread')


def help(cmds):
    message = ""
    command_list = ['var', 'delete', 'update', 'show', 'read', 'write', 'listen']
    if not len(cmds) > 3:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> pin i2c help [COMMAND]')
    try:
        return eval('Usage.{}_usage()'.format(cmds[3]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[3]))


def registry(cmds):
    blueprint = {"pinType": "i2c", "--name": "", "--scl": "", "--sda": "", "--baud": _find_value("i2c/baudrate"), "--address": ""}
    return CommonCommands(cmds).register(blueprint)


def delete(cmds):
    return CommonCommands(cmds).delete()        


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


def write(cmds):
    blueprint = {"--data": ""}
    blueprint = EngineTemplate.parameter_parser(cmds, blueprint)
    pin = CommonCommands(cmds).get_pin("i2c", cmds[3])

    if cmds[3] == pin["--name"] and "i2c" == pin["pinType"]:
        try:
            runner_pin = SoftI2C(scl=Pin(int(pin["--scl"])), sda=Pin(int(pin["--sda"])), freq=int(pin["--baud"]))
        except Exception as ex:
            return LOG.error(ex)
        try:
            for i in blueprint["--data"]:
                runner_pin.writeto(int(pin["--address"]), i)
            del runner_pin
            return LOG.info("Data is sent to given i2c port.")
        except Exception as ex:
            del runner_pin
            return LOG.error(ex)


def read(cmds):
    message = ""
    blueprint = {"--byte": "1"}
    blueprint = EngineTemplate.parameter_parser(cmds, blueprint)
    pin = CommonCommands(cmds).get_pin("i2c", cmds[3])
    rxData = bytes()
    try:
        runner_pin = SoftI2C(scl=Pin(int(pin["--scl"])), sda=Pin(int(pin["--sda"])), freq=int(pin["--baud"]))
    except Exception as ex:
        return LOG.error(ex)
    try:
        rxData = runner_pin.readfrom(int(pin["--address"]), int(blueprint["--byte"]))
        message = rxData.decode('utf-8')
        del runner_pin
        return message
    except Exception as ex:
        del runner_pin
        return LOG.error(ex)


def listen(cmds):
    if not len(cmds) > 3:
        LOG.error("Missing arguments(s)!")
        return
    pin = CommonCommands(cmds).get_pin("i2c", cmds[3])
    blueprint = {"--delay": "1", "--file": "", "--date": "1", "--end": "\n", "--loop": "-1"}
    listen_conf = EngineTemplate.parameter_parser(cmds, blueprint)
    thread_conf = {'delay': listen_conf['--delay'], 'loop': listen_conf['--loop'], 'type': 'i2c_listen', 'pin_name': cmds[3]}
    del blueprint
    if cmds[3] == pin["--name"] and "i2c" == pin["pinType"]:
        try:
            _gooz_start_function_thread(_i2c_listen_thread, (pin, listen_conf), thread_conf)
        except Exception as ex:
            LOG.error(ex)
            raise ex
    del listen_conf
    del thread_conf


def _i2c_listen_thread(pin, conf):
    rx_data = bytes()
    try:
        runner_pin = SoftI2C(
            scl=Pin(int(pin["--scl"])), sda=Pin(int(pin["--sda"])))
    except Exception as ex:
        LOG.error(ex)
        raise ex
        return "Error"
    try:
        rxData = runner_pin.readfrom(int(pin["--address"]), 1)
        if conf["--file"] == "":
            print('I2C "{}": "{}"'.format(
                pin["--name"], rx_data.decode('utf-8')))
        else:
            if conf["--date"] == "1":
                m_rtc = RTC()
                f = open(conf["--file"], "a")
                f.write("{} {}{}".format(runner_pin.readfrom(
                    int(pin["--address"]), 1), m_rtc.datetime(), conf["--end"]))
                f.close()
            else:
                f = open(conf["--file"], "a")
                f.write("{}{}".format(rx_data.decode('utf-8'), conf["--end"]))
                f.close()
    except Exception as ex:
        LOG.error(ex)
        raise ex
    del runner_pin
