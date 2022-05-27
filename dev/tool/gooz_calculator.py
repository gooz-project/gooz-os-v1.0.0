from etc.env.env_manager import find_val,delete_var

def calc(cmds):
    if len(cmds) > 2:
        if cmds[2] == ">":
            var_key = cmds[3]
            if not find_val(var_key):
                f = open("//etc/env/env_variables.txt","a")
                f.write(var_key+"="+str(eval(f'{cmds[1]}'))+"\n")
                f.close()
            else:
                delete_var(var_key)
                calc(cmds)
    else:
        try:
            return eval(f'{cmds[1]}')
        except Exception:
            return "Invalid or undefined operator!"