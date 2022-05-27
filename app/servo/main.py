from machine import Pin,PWM
import utime
from wifuxlogger import WifuxLogger as LOG
from engine.engine_template import EngineTemplate
import ujson
from dev.pin.core import CommonCommands as PinCommands

config_path="//app/servo/servoconfig.json"


class Servo_MotorUsage():
    
    @staticmethod
    def error_undefined_pin(pin_name):
        return LOG.error(f'There is no Servo pin named {pin_name}!')
    
    @staticmethod
    def var_usage():
        return LOG.info(' -> servo var --name [PIN NAME] -pin [PWM_PIN] ')
    
    @staticmethod
    def degree_usage():
        return LOG.info(' -> servo write [PIN NAME] [DEGREE]')+'\n'+LOG.info('[DEGREE] have to be between 0 and 180')
    
    @staticmethod
    def delete_usage():
        return LOG.info(' -> servo delete [PIN NAME]')+'\n'+LOG.info('servo delete command deletes registered Servo pins by pin_name')
    
    @staticmethod
    def show_usage():
        return LOG.info(' -> servo show')+'\n'+LOG.info('servo show command simply prints registered Servo pins')
    
    @staticmethod
    def update_usage():
        return LOG.info(' -> servo update [PIN NAME] --[PARAMETER_NAME] [NEW_PARAMETER]')+'\n'+LOG.info('updates registered Servo named [PIN NAME]')


def help(cmds):   
    message = ""
    command_list = ['var','show','delete','update','degree']
    if not len(cmds) > 2:
        for command in command_list:
            message += command
            message += '\n'
        return 'Commands:\n'+message+LOG.info('For more information about commands -> servo help [COMMAND]')
    try:
        return eval('Servo_MotorUsage.{}_usage()'.format(cmds[2]))
    except:
        return LOG.error('There is no help for "{}"!'.format(cmds[2]))


def var(cmds):
    blueprint={"pinType":"servo","--name":"","--pin":""}
    missing_arg = False
    temp = EngineTemplate.parameter_parser(cmds,blueprint)
    for key in temp:
        if temp[key] == "":
            missing_arg = True
            return LOG.error('Error while registering Servo pin!')+'\n'+LOG.error('Missing Argument(s)!')
    
    PinCommands(cmds, path=config_path,pin_type="servo").register(blueprint)
    return LOG.debug('The new Servo pin named "{}" successfully saved:\n{}'.format(blueprint["--name"],blueprint))


def delete(cmds):
    return PinCommands(cmds, path=config_path, pin_type="servo", pin_name=cmds[2]).delete()
        
        
def update(cmds):
    return PinCommands(cmds,config_path,pin_type="servo",pin_name=cmds[2]).update()


def show(cmds):
    return PinCommands(cmds,path=config_path,pin_type="servo").show()


def run(cmds):
    if not len(cmds)>1:
        return LOG.error("Please enter a command!")+'\n'+LOG.info("You can use 'servo help' for available commands!")
    if cmds[1][0] == '_':
        return "ERROR"
    try:
        return eval("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))
    except NameError:
        return LOG.error("There is a problem while running Servo command")+'\n'+LOG.error(f'Is the "{cmds[1]}" a Servo command?')+'\n'+LOG.info("You can use 'servo help' for available commands!")
    except Exception as ex:
        return LOG.error("There is a problem while running Servo command!")+'\n'+LOG.error(ex)+'\n'+LOG.error("You can use 'servo help' for available commands!")
    
    
def degree(cmds):
    blueprint = {}
    blueprint = EngineTemplate.parameter_parser(cmds,blueprint)
    pin = PinCommands(cmds,path=config_path,pin_type="servo").get_pin(cmds[0],cmds[2])
    
    if cmds[2] == pin["--name"] and pin["pinType"] == "servo":
        try:
            servo_pin = PWM(Pin(int(pin["--pin"])), freq = 50)
        except Exception as ex:
            return LOG.error(ex)
        try:
            servo_pin.duty(int((int(cmds[3])*5/9)+20))
        except Exception as ex:
            return LOG.error(ex)
        del servo_pin
        return LOG.info("The servo is succesfully executed.")
 
