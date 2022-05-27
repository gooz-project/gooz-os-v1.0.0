from wifuxlogger import WifuxLogger as LOG

class EnvSyntaxErrors:
    @staticmethod
    def equal_format_error():
        return LOG.error("There is a equal format syntax error")
    @staticmethod
    def var_not_found_error(var_key):
        return LOG.error("This env var not found -> {}".format(str(var_key)))
        
def write(cmds):
    try:
        if cmds[1] == "=":
            var_key = cmds[0][1:]
            cmd_str = " ".join(x for x in cmds)
            var_value = cmd_str.split("=")[1][1:]
            changed = False
            if not find_val(var_key):
                f = open("//etc/env/env_variables.txt","a")
                f.write(var_key+"="+var_value+"\n")
                f.close()
            else:
                delete_var(var_key)
                changed = True
                write(cmds)
        if changed:
            return LOG.info('The variable changed successfully: {}'.format(var_key+'='+var_value))
        else:
            return LOG.info('The variable added successfully: {}'.format(var_key+'='+var_value))
    except Exception:
        return EnvSyntaxErrors.equal_format_error()
        
def export(cmds):
    try:
        if "=" in cmds[1]:
            var_key = cmds[1].split("=")[0]
            cmd_str = " ".join(x for x in cmds)
            var_value = cmd_str.split("=")[1]
            changed = False
            if not find_val(var_key):
                f = open("//etc/env/env_variables.txt","a")
                f.write(var_key+"="+var_value+"\n")
                f.close()
            else:
                delete_var(var_key)
                export(cmds)
                changed=True
                
        if changed:
            return LOG.info('The variable changed successfully: {}'.format(var_key+'='+var_value))
        else:
            return LOG.info('The variable added successfully: {}'.format(var_key+'='+var_value))
    except Exception:
        return EnvSyntaxErrors.equal_format_error()

def unset(cmds):
    if len(cmds)>1:
        var_key = cmds[1]
        delete_var(var_key)
    return LOG.debug("Variable {} successfully deleted")
    
def delete_var(var_key):
    if not find_val(var_key):
        return EnvSyntaxErrors.var_not_found_error(var_key)
    else:
        f = open("//etc/env/env_variables.txt","r")
        lines = f.readlines()
        f.close()
        new_lines = []
        for line in lines:
            if not line.split("=")[0] == var_key:
                new_lines.append(line)
        f = open("//etc/env/env_variables.txt","w")
        for line in new_lines:
            f.write(line)
        f.close()
        
def find_val(var_key):
    f = open("//etc/env/env_variables.txt","r")
    env_vars = f.readlines()
    f.close()
    founded = False
    var = ""
    for line in env_vars:
        if line.split("=")[0] == var_key:
            var_list = line.split("=")[1:]
            for x in var_list:
                var += x
            founded = True
            break
    if not founded:
        return False
    else:
        return var.rstrip()
        
def show(cmds):
    f = open("//etc/env/env_variables.txt","r")
    env_vars = f.readlines()
    f.close()
    message = ""
    if len(cmds) == 1:
        for i in env_vars:
            message += i + ""
        return message.rstrip()
    else:
        founded = False
        for line in env_vars:
            if line.split("=")[0] == cmds[1]:
                var_list = line.split("=")[1:]
                var = ""
                for x in var_list:
                    var += x
                founded = True
                return var.rstrip()
        if not founded:
            return LOG.error('The env var refers to "{}" not found'.format(cmds[1]))