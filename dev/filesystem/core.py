import os
from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG


class Usage():
    @staticmethod
    def ls_usage():
        message = LOG.info('Usage -> ls [PATH] -> lists without any hidden files') + "\n"
        message += LOG.info('-> ls -a [PATH] -> lists with all hidden files') + "\n"
        message += LOG.info('If [PATH] is not entered lists files and directories in current directory')
        return message
    
    @staticmethod
    def pwd_usage():
        message = LOG.info('Usage -> pwd') + "\n" + LOG.info('prints the current working directory')
        return message

    @staticmethod
    def cd_usage():
        message = LOG.info('Usage -> cd [DIRECTORY] -> goes [DIRECTORY] path') + "\n" + LOG.info('-> cd .. -> goes upper directory')
        return message

    @staticmethod
    def rm_usage():
        message = LOG.info('Usage -> rm [FILE]') + "\n" + LOG.info('deletes entered [FILE] in current directory or given path (/[DIR]/[FILE])')
        return message

    @staticmethod
    def rmdir_usage():
        message = LOG.info('Usage -> rmdir [DIRECTORY]') + "\n"
        message += LOG.info('deletes entered directory recursively named [DIRECTORY] in current directory or given path (/[DIR]/[DIRECTORY])')
        return message
    
    @staticmethod
    def cat_usage():
        message = LOG.info('Usage -> cat [FILE]') + "\n"
        message += LOG.info('reads the content of [FILE] in the current directory or given path (/[DIR]/[FILE])')
        return message
    
    @staticmethod
    def clear_usage():
        message = LOG.info('Usage -> clear') + "\n" + LOG.info('clears terminal')
        return message

    @staticmethod
    def echo_usage():
        message = LOG.info('Usage -> echo [DATA] -> prints data to terminal') + "\n"
        message += LOG.info('-> echo [DATA] > [FILE] -> prints data to a new file') + "\n"
        message += LOG.info('-> echo [DATA] >> [FILE] -> adds data to already an existing file')
        return message
    
    @staticmethod
    def touch_usage():
        message = LOG.info('Usage -> touch [FILE]') + "\n"
        message += LOG.info('creates a new empty [FILE] in the current directory or given path (/[DIR]/[FILE])')
        return message
    
    @staticmethod
    def mkdir_usage():
        message = LOG.info('Usage -> mkdir [FOLDER]') + "\n"
        message += LOG.info('creates a new empty [FOLDER] in the current directory or given path (/[DIR]/[FOLDER])')
        return message

    @staticmethod
    def mv_usage():
        message = LOG.info('Usage -> mv [FILE1] [FILE2] -> renames [FILE1] to [FILE2]') + "\n"
        message += LOG.info('-> mv [FILE1] [FOLDER] [FILE2] -> moves [FILE1] to [FOLDER] as [FILE2]')
        return message
    
    @staticmethod
    def cp_usage():
        message = LOG.info('Usage -> cp [FILE1] [FILE2] -> copies [FILE1] as [FILE2]') + "\n"
        message += LOG.info('Usage -> cp [FILE1] [FOLDER] [FILE2]-> copies [FILE1] to the bottom of the [FOLDER] as [FILE2]')
        return message
    
    @staticmethod
    def list_usage():
        message = LOG.info('Usage -> list') + "\n" + LOG.info('lists available functions')
        return message


def help(cmds):
    command_list = ['ls', 'pwd', 'cd', 'rm', 'rmdir', 'cat',
                    'clear', 'echo', 'touch', 'mkdir', 'mv', 'cp', 'list']
    if not len(cmds) > 1:
        message = "Commands: " + "\n"
        for command in command_list:
            message += command + "\n"
        message += LOG.info("For more information about commands -> help [COMMAND]")
        return message.rstrip()
    try:
        return eval(f'Usage.{cmds[1]}_usage()')
    except:
        return LOG.error(f'There is no help for "{cmds[1]}"!')


def run(cmds):
    return eval("{}({})".format(cmds[0], EngineTemplate.exec_formatter_api(cmds)))


def ls(cmds):
    if len(cmds) == 1:
        ls = os.listdir()
        for i in os.listdir():
            if i[0] == '.':
                ls.remove(i)
        return LOG.info("{}".format(ls))
    if len(cmds) == 2 and cmds[1] == '-a':
        return LOG.info("{}".format(os.listdir()))
    if len(cmds) == 2 and cmds[1] != '-a':
        ls = os.listdir(os.getcwd()+cmds[1])
        for i in os.listdir(os.getcwd()+cmds[1]):
            if i[0] == '.':
                ls.remove(i)
        return LOG.info("{}".format(ls))
    if len(cmds) == 3 and cmds[2] == '-a':
        return LOG.info("{}".format(os.listdir(os.getcwd()+cmds[1])))


def pwd(cmds):
    return LOG.info("{}".format(os.getcwd()))


def cd(cmds):
    try:
        os.chdir(cmds[1])
        return LOG.debug("Directory successfully changed")
    except Exception:
        return LOG.error("Directory not found")


def rm(cmds):
    try:
        for i in range(1, len(cmds)):
            os.remove(cmds[i])
        return LOG.debug("File(s) successfully deleted.")
    except Exception:
        return LOG.error("File(s) couldn't be deleted.")


def rmdir(cmds):
    try:
        os.rmdir(cmds[1])
    except Exception:
        deltree(os.getcwd()+cmds[1])
    return LOG.debug("Directory {} successfully deleted.".format(cmds[1]))


def deltree(target):
    for d in os.listdir(target):
        try:
            deltree(target + "/" + d)
        except OSError:
            os.remove(target + "/" + d)
    os.rmdir(target)


def cat(cmds):
    if cmds[1][0] == ".":
        break_flag = 0
        str_temp_cat = ""
        pwd = os.getcwd()
        for i in cmds[1]:
            if i == "." and break_flag == 0:
                break_flag = 1
                continue
            else:
                str_temp_cat += i
        path = pwd+str_temp_cat
        message = read(path)
    elif cmds[1][0] == "/":
        message = read(cmds[1])
    else:
        pwd = os.getcwd()
        path = pwd+"/"+cmds[1]
        message = read(path)
    return message.rstrip()

def read(path):
    try:
        f = open(path, 'r', encoding='utf-8')
        data = f.read()
        f.close()
        return LOG.info("\n{}".format(data))
    except:
        return LOG.error("File does not exist.")


def clear(cmds):
    return ("\n" * 100)


def echo(cmds):
    try:
        if '>' in cmds:
            for i in range(1,len(cmds)):
                if cmds[i] == '>':
                    with open(cmds[i+1],'w',encoding='utf-8') as file:
                        a = cmds[1:i]
                        for words in a:
                            file.write("{} ".format(words))
                        file.close()
                    return LOG.debug("File successfully created.")
        elif '>>' in cmds:
            for i in range(1,len(cmds)):
                if cmds[i] == '>>' and (cmds[i+1]) in os.listdir():
                    with open(cmds[i+1],'a',encoding='utf-8') as file:
                        a = cmds[1:i]
                        for words in a:
                            file.write("{} ".format(words))
                        file.close()
                    return LOG.debug("File successfully updated.")
                elif cmds[i] == '>>' and (cmds[i+1]) not in os.listdir():
                    return LOG.error("No such a file")
        else:
            message = ""
            for i in range(1,len(cmds)):
                message += cmds[i]+" "
            return message
    except Exception as ex:
        return LOG.error("{}".format(ex))


def touch(cmds):
    try:
        if cmds[1][0] == "/":
            write(cmds[1])
        else:
            pwd = os.getcwd()
            path = pwd+"/"+cmds[1]
            write(path)
        return LOG.debug("File {} successfully created.".format(cmds[1]))
    except Exception as ex:
        return LOG.error("{}".format(ex))


def write(path):
    try:
        f = open(path, 'w', encoding='utf-8')
        f.close()
    except:
        return LOG.error("File is not created.")


def mkdir(cmds):
    try:
        for i in range(1, len(cmds)):
            os.mkdir(cmds[i])
        return LOG.debug("Directory(s) successfully created.")
    except Exception:
        return LOG.error("Directory(s) couldn't be created.")


def mv(cmds):
    if '.' in cmds[2]:
        os.rename(cmds[1], cmds[2])
        return LOG.debug("File {} successfully renamed.".format(cmds[1]))
    elif '.' not in cmds[2]:
        with open(cmds[2]+"/"+cmds[3], 'w') as file1:
            with open(cmds[1], 'r') as file2:
                file1.write(file2.read())
                file1.close()
            file2.close()
        os.remove(cmds[1])
        return LOG.debug("File {} successfully moved to the bottom of the {}.".format(cmds[1],cmds[2]))


def cp(cmds):
    if '.' in cmds[2]:
        with open(cmds[2], 'w') as file1:
            with open(cmds[1], 'r') as file2:
                file1.write(file2.read())
                file1.close()
            file2.close()
        return LOG.debug("File {} successfully copied.".format(cmds[1],cmds[2]))
    elif '.' not in cmds[2]:
        with open(cmds[2]+"/"+cmds[3], 'w') as file1:
            with open(cmds[1], 'r') as file2:
                file1.write(file2.read())
                file1.close()
            file2.close()
        return LOG.debug("File {} successfully copied to the bottom of the {}.".format(cmds[1],cmds[2],cmds[3]))


def list(cmds):
    try:
        functions = ["pin", "list", "clear", "usage", "calc", "wifi", "env", "unset", "pkg", "conf", "goozshell", "delay", "curl", "mkdir", "pwd", "cd", "ls", "rm", "rmdir", "cat", "history", "shutdown", "reset", "touch", "echo", "cp", "mv"]
        message = ""
        message = LOG.info("Available functions") + "\n"
        for i in functions:
            message += i + "\n"
        return message.rstrip()
    except Exception as ex:
        return LOG.error("{}".format(ex))
