from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
from machine import Pin, PWM
from dev.pin.core import CommonCommands
from etc.config.core import _find_value


class Usage():
    @staticmethod
    def var_usage():
        return LOG.info('Usage -> pin var pwm --name [PIN_NAME] --pin [PIN_NUMBER] --freq [PWM_FREQUENCY]')+'\n'+LOG.info('Sets PWM frequency from 1Hz to 40MHz with [PWM_FREQUENCY].Default pwm frequency is 5000Hz.')

    @staticmethod
    def delete_usage():
        return LOG.info('Usage -> pin pwm delete [PIN_NAME]')+'\n'+LOG.info('deletes registered pwm pin named [PIN_NAME]')+'\n'+LOG.info('To delete all registered pwm pins -> pin pwm delete all')

    @staticmethod
    def update_usage():
        return LOG.info('Usage -> pin pwm update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]')+'\n'+LOG.info('updates the [VALUE_TO_CHANGE] value of the pwm pin named [PIN_NAME] to [NEW_VALUE]')

    @staticmethod
    def show_usage():
        message = ""
        message += LOG.info('Usage -> pin pwm show')+'\n'
        message += LOG.info('shows all registered pwm pins')+'\n'
        message += LOG.info('Usage -> pin pwm show [PARAMETER]:[VALUE_TO_SEARCH_FOR]')+'\n'
        message += LOG.info('shows specific pwm pins')
        return message

    @staticmethod
    def write_usage():
        return LOG.info('Usage -> pin pwm write [PIN_NAME] [PWM_DUTY_CYCLE]')+'\n'+LOG.info('writes  [PWM_DUTY_CYCLE]  to pwm pin named [PIN_NAME]')+'\n'+LOG.info('[PWM_DUTY_CYCLE] sets duty cycle from 0 to 1023 (0v - 3.3v).If duty cycle is 0,pwm pin is closed.')

    @staticmethod
    def close_usage():
        return LOG.info('Usage -> pin pwm close [PIN_NAME]')+'\n'+LOG.info('Turns off the running pwm pin named [PIN NAME]')


def help(cmds):
    message = ""
    command_list = ['var', 'delete', 'update', 'show', 'write', 'close']
    if not len(cmds) > 3:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> pin pwm help [COMMAND]')
    try:
        return eval('Usage.{}_usage()'.format(cmds[3]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[3]))


def delete(cmds):
    return CommonCommands(cmds).delete()        


def registry(cmds):
    blueprint = {"pinType": "pwm", "--name": "","--pin": "", "--freq": _find_value("pwm/freq")}
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
    pins = CommonCommands(cmds).get_pin(cmds[1], cmds[3])
    try:
        runner_pin = PWM(Pin(int(pins["--pin"])),freq=int(pins["--freq"]), duty=int(cmds[4]))
        del runner_pin
        return "PWM value is writed to the pin."
    except Exception as ex:
        return LOG.error(ex)


def close(cmds):
    pin = CommonCommands(cmds).get_pin(cmds[1], cmds[3])
    try:
        runner_pin = PWM(Pin(int(pin["--pin"])),freq=int(pin["--freq"]), duty=0)
        runner_pin.deinit()
        return "The PWM Pin is closed."
    except Exception as ex:
        return LOG.error(ex)
