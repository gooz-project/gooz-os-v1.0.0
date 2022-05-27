from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
from machine import Pin
from dev.pin.core import CommonCommands


class Usage():
    @staticmethod
    def var_usage():
        return LOG.info('Usage -> pin var gpio --name [PIN_NAME] --pin [PIN_NUMBER] --type [GPIO_TYPE]')+'\n'+LOG.info('[GPIO_TYPE] can be OUT, IN, ALT, OPENDRAIN, ALTOPENDRAIN')

    @staticmethod
    def delete_usage():
        return LOG.info('Usage -> pin gpio delete [PIN_NAME]')+'\n'+LOG.info('deletes registered gpio pin named [PIN_NAME]')+'\n'+LOG.info('To delete all registered gpio pins -> pin gpio delete all')

    @staticmethod
    def update_usage():
        return LOG.info('Usage -> pin gpio update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]')+'\n'+LOG.info('updates the [VALUE_TO_CHANGE] value of the gpio pin named [PIN_NAME] to [NEW_VALUE]')

    @staticmethod
    def show_usage():
        return LOG.info('Usage -> pin gpio show')+'\n'+LOG.info('shows all registered gpio pins')+'\n'+LOG.info('Usage -> pin gpio show [PARAMETER]:[VALUE_TO_SEARCH_FOR]')+'\n'+LOG.info('shows specific gpio pins')

    @staticmethod
    def write_usage():
        return LOG.info('Usage -> pin gpio write [PIN_NAME] [VALUE]')+'\n'+LOG.info('[VALUE] can be HIGH(1) or LOW(0)')

    @staticmethod
    def read_usage():
        return LOG.info('Usage -> pin gpio read [PIN_NAME]')+'\n'+LOG.info('Reads the digital value of pin named [PIN_NAME]')


def help(cmds):
    message = ""
    command_list = ['registry', 'delete', 'update', 'show', 'write']
    if not len(cmds) > 3:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> pin gpio help [COMMAND]')
    try:
        return eval('Usage.{}_usage()'.format(cmds[3]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[3]))


def delete(cmds):
    return CommonCommands(cmds).delete()        


def registry(cmds):
    blueprint = {"pinType": "gpio", "--name": "", "--pin": "", "--type": ""}
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
    pin = CommonCommands(cmds).get_pin("gpio", cmds[3])
    try:
        runner_pin = Pin(int(pin["--pin"]),eval("Pin.{}".format(pin["--type"])))
    except Exception as ex:
        LOG.error(ex)
        raise ex
    if cmds[4] == "HIGH":
        cmds[4] = "1"
    elif cmds[4] == "LOW":
        cmds[4] = "0"
    try:
        runner_pin.value(int(cmds[4]))
        del runner_pin
        return "Data writed to given pin!"
    except Exception as ex:
        del runner_pin
        return LOG.error(ex)


def read(cmds):
    message = ""
    pin = CommonCommands(cmds).get_pin("gpio", cmds[3])
    try:
        runner_pin = Pin(int(pin["--pin"]),eval("Pin.{}".format(pin["--type"])))
    except Exception as ex:
        del runner_pin
        return LOG.error(ex)
    message = runner_pin.value()
    del runner_pin
    return message
