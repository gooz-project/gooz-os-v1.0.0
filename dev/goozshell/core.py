from engine.engine_template import EngineTemplate
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG

def run(cmds): 
    f = open(cmds[1],"r")
    commands = f.readlines()
    message = ""
    for command in commands:
        command = command.rstrip()
        cmd_array = GoozEngine.parser(command)
        data = EngineTemplate(cmd_array)
        message += str(data.registry())+'\n'
    return message