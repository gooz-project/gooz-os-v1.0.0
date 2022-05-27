from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
import ujson

main_pins = ["gpio", "adc", "pwm", "spi", "i2c", "uart"]


class CommonCommands():
    def __init__(self, cmds, path="//dev/pin/pinconfig.json", pin_type="", pin_name="", main=True):
        self.cmds = cmds
        self.path = path
        if pin_type == "":
            self.pin_type = cmds[1]
        else:
            self.pin_type = pin_type
        if pin_name == "" and len(cmds) > 3:
            self.pin_name = cmds[3]
        else:
            self.pin_name = pin_name
        self.main = self.pin_type in main_pins

    def register(self, blueprint):
        message = ""
        blueprint = EngineTemplate.parameter_parser(self.cmds, blueprint)
        missing_arg = False
        self.main = self.cmds[2] in main_pins
        for key in blueprint:
            if blueprint[key] == "":
                missing_arg = True
                break
        if missing_arg:
            message += LOG.error("Error while registering {} pin!\n".format(blueprint["pinType"]))
            message += LOG.error("Missing Argument(s)!\n")
            if self.main:
                message += LOG.info("You can use 'pin {} help' command for usage!".format(blueprint["pinType"]))
            else:
                message += LOG.info("You can use '{} help' command for usage!".format(blueprint["pinType"]))
            return message
        if self.main and self.get_pin(self.cmds[2], blueprint['--name']):
            message += LOG.error('The {} pin named "{}" already exists!'.format(self.cmds[2], blueprint['--name']))
            return message
        registered_set = self.returnerload()
        registered_set.append(blueprint)
        with open(self.path, "w") as fp:
            ujson.dump(registered_set, fp)
            fp.close()
        if self.main:
            message += LOG.info('The {} pin named {} successfully registered\n{}'.format(self.pin_type, blueprint['--name'], blueprint))
        return message

    def delete(self):
        payload = ""
        payload = self.returnerload()
        founded = False
        with open(self.path, 'w') as fp:
            try:
                for i in range(0, len(self.cmds)):
                    if self.cmds[i] == 'delete':
                        if self.cmds[i+1] == 'all':
                            payload = [pin for pin in payload if pin['pinType'] != self.pin_type]
                            founded = True
                            break
                        else:
                            break
                for pin in payload:
                    if pin["--name"] == self.pin_name and pin["pinType"] == self.pin_type:
                        payload.remove(pin)
                        founded = True
                        break
                ujson.dump(payload, fp)
                fp.close()
                if founded:
                    return LOG.info("The pin(s) deleted succesfully.")
                else:
                    return LOG.error("The pin named {} does not exist!".format(self.pin_name))
            except Exception as ex:
                return LOG.error(ex)+"\nCouldn't delete the pin"

    def update(self):
        blueprint = {}
        payload = self.returnerload()
        for pin in payload:
            if pin["--name"] == self.pin_name and pin["pinType"] == self.pin_type:
                blueprint = pin
                self.delete()
                break
        if blueprint == {}:
            return LOG.error("There is no parameter to update!")
        blueprint = EngineTemplate.parameter_parser(self.cmds, blueprint)
        payload = self.returnerload()
        payload.append(blueprint)
        with open(self.path, "w") as fp:
            ujson.dump(payload, fp)
            fp.close()
        return LOG.info("The pin is updated.")

    def show(self):
        message = ""
        flag = False
        payload = self.returnerload()
        if not len(payload) > 0:
            return LOG.info("No registered pins")
        if self.main and len(self.cmds) > 3:
            key = self.cmds[3].split(':')[0]
            content = self.cmds[3].split(':')[1]
        elif not self.main and len(self.cmds) > 2:
            key = self.cmds[2].split(':')[0]
            content = self.cmds[2].split(':')[1]
        else:
            for pin in payload:
                if pin["pinType"] == self.pin_type:
                    message += LOG.info(pin)+'\n'
                    flag = True
            if flag == False:
                return LOG.info("No {} pins".format(self.pin_type))
            else:
                return message.rstrip()
        for pin in payload:
            if pin["--{}".format(key)] == content and pin["pinType"] == self.pin_type:
                message += LOG.info(pin) + '\n'
                flag = True
        if flag == False:
            return LOG.info("There is no {} pin matching the searched parameter value.".format(self.pin_type))
        return message.rstrip()

    def returnerload(self):
        payload = ""
        try:
            with open(self.path, "r") as fp:
                payload = fp.read()
                fp.close()
            payload = ujson.loads(payload)
        except OSError:
            with open(self.path, "w")as fp:
                fp.write('[]')
                fp.close()
            payload = ujson.loads('[]')
        return payload

    def get_pin(self, pin_type, pin_name):
        payload = self.returnerload()
        founded = False
        for pin in payload:
            if pin["--name"] == pin_name and pin["pinType"] == pin_type:
                founded = True
                return pin
        if not founded:
            return False
        

def run(cmds):
    return eval("{}({})".format(cmds[1], EngineTemplate.exec_formatter_api(cmds)))


def var(cmds):
    exec("import dev.pin.gooz_pin_{} as _{}".format(cmds[2], cmds[2]))
    return eval("_{}.registry({})".format(cmds[2], EngineTemplate.exec_formatter_api(cmds)))
    

def gpio(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_gpio as gpioclass")
    message = eval("gpioclass.run({})".format(cmds))
    exec("del gpioclass")
    return message


def pwm(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_pwm as pwmclass")
    message = eval("pwmclass.run({})".format(cmds))
    exec("del pwmclass")
    return message


def adc(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_adc as adcclass")
    message = eval("adcclass.run({})".format(cmds))
    exec("del adcclass")
    return message


def spi(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_spi as spiclass")
    message = eval("spiclass.run({})".format(cmds))
    exec("del spiclass")
    return message

    
def i2c(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_i2c as i2cclass")
    message = eval("i2cclass.run({})".format(cmds))
    exec("del i2cclass")
    return message

    
def uart(cmds):
    message = ""
    exec("import dev.pin.gooz_pin_uart as uartclass")
    message = eval("uartclass.run({})".format(cmds))
    exec("del uartclass")
    return message
