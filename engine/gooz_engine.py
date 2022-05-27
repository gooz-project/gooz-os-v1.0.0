from engine.engine_template import EngineTemplate
from gc import collect
from wifuxlogger import WifuxLogger as LOG
gc_handler = 0


class GoozEngine():

    @staticmethod
    def run(commands):
        global gc_handler
        gc_handler += 1
        if gc_handler == 10:
            collect()
            gc_handler = 0
        if commands == "":
            return
        command_str = ""
        command_array = []
        str_flag = 0
        for i in commands:
            if i == "\"":
                if str_flag == 0:
                    str_flag = 1
                elif str_flag == 1:
                    str_flag = 0
            elif i == " " and str_flag == 0:
                command_array.append(command_str)
                command_str = ""
            else:
                command_str += i
        command_array.append(command_str)
        command_str = ""
        data = EngineTemplate(command_array)
        message = data.registry()
        print(message)
        return message

    @staticmethod
    def parser(commands):
        command_str = ""
        command_array = []
        str_flag = 0
        for i in commands:
            if i == "\"":
                if str_flag == 0:
                    str_flag = 1
                elif str_flag == 1:
                    str_flag = 0
            elif i == " " and str_flag == 0:
                command_array.append(command_str)
                command_str = ""
            else:
                command_str += i
        command_array.append(command_str)
        command_str = ""
        return command_array
