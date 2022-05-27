from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
import ujson
from machine import UART, RTC
from dev.tool.gooz_thread import _gooz_start_function_thread
from etc.config.core import _find_value
from dev.pin.core import CommonCommands


class Usage():
    @staticmethod
    def var_usage():
        return LOG.info('Usage -> pin var uart --name [PIN_NAME] --id [UART_ID] --baud [BAUDRATE]')+'\n'+LOG.info('[UART_ID] can be 0 ,1 or 2')+'\n'+LOG.info('[BAUDRATE] is 9600 as default. Also it can be assigned manually.')

    @staticmethod
    def delete_usage():
        return LOG.info('Usage -> pin uart delete [PIN_NAME]')+'\n'+LOG.info('deletes registered uart pin named [PIN_NAME]')+'\n'+LOG.info('To delete all registered uart pins -> pin uart delete all')

    @staticmethod
    def update_usage():
        return LOG.info('Usage -> pin uart update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]')+'\n'+LOG.info('updates the [VALUE_TO_CHANGE] value of the uart pin named [PIN_NAME] to [NEW_VALUE]')

    @staticmethod
    def show_usage():
        message = ""
        message += LOG.info('Usage -> pin uart show') + '\n'
        message += LOG.info('shows all registered uart pins') + '\n'
        message += LOG.info('Usage -> pin uart show [PARAMETER]:[VALUE_TO_SEARCH_FOR]') + '\n'
        message += LOG.info('shows specific uart pins')
        return message

    @staticmethod
    def write_usage():
        return LOG.info('Usage -> pin uart write [PIN_NAME] --data [TX_DATA]')+'\n'+LOG.info('sends [TX_DATA] to uart pin named [PIN_NAME]')

    @staticmethod
    def read_usage():
        return LOG.info('Usage -> pin uart read [PIN_NAME] ')+'\n'+LOG.info('reads last taken data from uart pin named [PIN_NAME]')

    @staticmethod
    def listen_usage():
        return LOG.info('Usage -> pin uart listen [UART_NAME]')+'\n'+LOG.info('reads datas continuously in thread from uart pin named [PIN_NAME]')


def help(cmds):
    message = ""
    command_list = ['var', 'delete', 'update', 'show', 'write', 'read', 'listen']
    if not len(cmds) > 3:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> pin uart help [COMMAND]')
    try:
        return eval('Usage.{}_usage()'.format(cmds[3]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[3]))


def delete(cmds):
    return CommonCommands(cmds).delete()        


def registry(cmds):
    blueprint = {"pinType": "uart", "--name": "", "--id": "", "--baud": _find_value("uart/baudrate")}
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


def write(cmds):
    if not len(cmds) > 4:
        return LOG.error("Missing Argument(s)")
    blueprint = {"--data": ""}
    blueprint = EngineTemplate.parameter_parser(cmds, blueprint)
    pin = CommonCommands(cmds).get_pin("uart", cmds[3])
    if cmds[3] == pin["--name"] and "uart" == pin["pinType"]:
        try:
            runner_pin = UART(int(pin["--id"]), baudrate=int(pin["--baud"]))
            runner_pin.write(blueprint["--data"])
            del runner_pin
            return LOG.debug(f'"{blueprint["--data"]}" is sent to the uart pin named "{cmds[3]}"')
        except Exception as ex:
            return LOG.error(ex)


def read(cmds):
    pin = CommonCommands(cmds).get_pin("uart", cmds[3])
    rxData = bytes()
    if cmds[3] == pin["--name"] and "uart" == pin["pinType"]:
        try:
            runner_pin = UART(int(pin["--id"]), baudrate=int(pin["--baud"]))
            while True:
                if runner_pin.any() > 0:
                    rxData = runner_pin.read().rstrip().decode('utf-8')
                    del runner_pin
                    return rxData
        except Exception as ex:
            return LOG.error(ex)


def listen(cmds):
    if not len(cmds) > 3:
        return LOG.error("Please enter pin name!")
    pin = CommonCommands(cmds).get_pin("uart", cmds[3])
    blueprint = {"--delay": "1", "--file": "", "--date": "1", "--end": "\n", "--loop": "-1"}
    listen_conf = EngineTemplate.parameter_parser(cmds, blueprint)
    thread_conf = {'delay': listen_conf['--delay'], 'loop': listen_conf['--loop'], 'type': 'uart_listen', 'pin_name': cmds[3]}
    del blueprint
    if cmds[3] == pin["--name"] and "uart" == pin["pinType"]:
        try:
            _gooz_start_function_thread(_uart_listen_thread, (pin, listen_conf), thread_conf)
            del listen_conf
            del thread_conf
        except Exception as ex:
            del listen_conf
            del thread_conf
            return LOG.error(ex)


def _uart_listen_thread(pin, conf):
    try:
        runner_pin = UART(int(pin["--id"]), baudrate=int(pin["--baud"]))
        rx_data = bytes()
        while True:
            if runner_pin.any() > 0:
                rx_data = runner_pin.read()
                break
        if conf["--file"] == "":
            print('Uart "{}": "{}"'.format(
                pin["--name"], rx_data.decode('utf-8')))
        else:
            if conf["--date"] == "1":
                m_rtc = RTC()
                f = open(conf["--file"], "a")
                f.write("{} {}{}".format(runner_pin.read(),
                        m_rtc.datetime(), conf["--end"]))
                f.close()
            else:
                f = open(conf["--file"], "a")
                f.write("{}{}".format(rx_data.decode('utf-8'), conf["--end"]))
                f.close()
    except Exception as ex:
        LOG.error(ex)
        raise ex
    del runner_pin
