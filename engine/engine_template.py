import sys
import os
from time import sleep as delay
from wifuxlogger import WifuxLogger as LOG
history = []


class EngineErrors:
    @staticmethod
    def command_not_found():
        return LOG.error("There is no command")


class EngineTemplate():
    _filesystem_list = ["help", "ls", "pwd", "cd", "rm", "rmdir","cat", "clear", "echo", "touch", "mkdir", "mv", "cp", "list"]
    _wifi_list = ["wifi"]
    _engine_commands = ["shutdown", "reset", "history"]
    _tool_list = ["usage", "calc", "rtc", "cpu_temp", "hall", "thread", "client"]
    
    
    def __init__(self, cmds):
        self.cmds = cmds
        
        
    def registry(self):
        try:
            if "$" == self.cmds[0][0] and len(self.cmds) > 1:
                if self.cmds[1] == "=":
                    exec("import etc.env.env_manager as env")
                    return eval("env.write({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "export":
                exec("import etc.env.env_manager as env")
                return eval("env.export({})".format(self.exec_formatter(self.cmds)))
            elif self.check_env_var(self.cmds):
                for i in self.check_env_var(self.cmds):
                    self.cmds = self.env_var_parser(self.cmds, i)
            if self.cmds[0] in self._filesystem_list:
                exec("import dev.filesystem.core as fsos")
                return eval("fsos.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] in self._wifi_list:
                exec("import dev.wifi.core as wfos")
                return eval("wfos.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] in self._engine_commands:
                return eval("EngineTemplate.{}()".format(self.cmds[0], self.exec_formatter(self.cmds)))
            elif self.cmds[0] in self._tool_list:
                exec("import dev.tool.core as tos")
                return eval("tos.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "pin":
                exec("import dev.pin.core as pinlib")
                return eval("pinlib.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "env":
                exec("import etc.env.env_manager as env")
                return eval("env.show({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "unset":
                exec("import etc.env.env_manager as env")
                return eval("env.unset({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "pkg":
                exec("import dev.packager.core as package")
                return eval("package.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "conf":
                exec("import etc.config.core as cfos")
                return eval("cfos.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "goozshell":
                exec("import dev.goozshell.core as shell")
                return eval("shell.run({})".format(self.exec_formatter(self.cmds)))
            elif self.cmds[0] == "delay":
                delay(float(self.cmds[1]))
            else:
                exec("import app."+self.cmds[0]+".main as command")
                return eval("command.run({})".format(self.exec_formatter(self.cmds)))
        except Exception as ex:
            return LOG.error("{}".format(ex))+"\n"+(EngineErrors.command_not_found())

    def exec_formatter(self, cmds):
        cmd_temp = "["
        for i in range(len(cmds)-1):
            cmd_temp += "'{}',".format(cmds[i])
            history.append(cmds[i])
        cmd_temp += "'{}'".format(cmds[len(cmds)-1])
        history.append(cmds[len(cmds)-1])
        history.append(",")
        cmd_temp += "]"
        return cmd_temp

    def env_var_parser(self, cmds, ind):
        import etc.env.env_manager as env
        var_key = cmds[ind][1:]
        var_value = env.find_val(var_key)
        if not var_value:
            raise Exception("This env var not found -> {}".format(cmds[ind]))
        else:
            if " " in var_value:
                del cmds[ind]
                for x in range(len(var_value.split(" "))):
                    cmds.insert(ind+x, var_value.split(" ")[x])
            else:
                del cmds[ind]
                cmds.insert(ind, var_value)
            return cmds

    def check_env_var(self, cmds):
        env_var_list = []
        for i in range(len(cmds)):
            if "$" == cmds[i][0]:
                env_var_list.append(i)
        return env_var_list

    @staticmethod
    def exec_formatter_api(cmds):
        cmd_temp = "["
        for i in range(len(cmds)-1):
            cmd_temp += "'{}',".format(cmds[i])
        cmd_temp += "'{}'".format(cmds[len(cmds)-1])
        cmd_temp += "]"
        return cmd_temp

    @staticmethod
    def shutdown():
        try:
            import dev.tool.gooz_client as gooz_client
            gooz_client.client.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
            gooz_client.client.send('System is shut down.')
            gooz_client.client.close()
        except:
            pass
        print(LOG.warning("System is shut down."))
        sys.exit()

    @staticmethod
    def reset():
        from machine import reset
        print(LOG.warning("System is resetting"))
        reset()

    @staticmethod
    def parameter_parser(cmds, parameter_blueprints={}):
        for i in range(len(cmds)):
            if "--" in cmds[i]:
                parameter_blueprints[cmds[i]] = cmds[i+1]
            elif "-" in cmds[i]:
                parameter_blueprints[cmds[i]] = "1"
        return parameter_blueprints

    def history():
        message = ""
        clean_str = ""
        for i in range(0, len(history)):
            if history[i] == ',':
                clean_str = ""
            else:
                clean_str += history[i]
                clean_str += " "
                message += clean_str
                message += '\n'
        return (LOG.info("--History--\n")+message).rstrip()
