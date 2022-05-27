from engine.gooz_engine import GoozEngine
from os import getcwd

login_flag = False

def start(username,machine):
    while login_flag:
        command = input(username+"@"+machine+":{} -> ".format(getcwd()))
        GoozEngine.run(command)