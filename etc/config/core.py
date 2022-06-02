from engine.engine_template import EngineTemplate
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG
import json

class ConfErrors:
    @staticmethod
    def no_key(key):
        return LOG.error('There is no key for "{}" !'.format(str(key)))
    def key_not_refer_str(key):
        message = LOG.error('The key "{}" is not refer a str!'.format(str(key))) + "\n"
        message += LOG.error('A dict is not changeable directly!')
        return message
        
def run(cmds):
    if cmds[1][0] =="_":
        return "OK"
    return eval("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def _load():
    config_file = open('//etc/config/configures.txt','r')
    data = json.loads(config_file.read())
    config_file.close()
    return data

def _find_value(path):
    path_list = path.split('/')
    config_file = open('//etc/config/configures.txt','r')
    data = json.loads(config_file.read())
    config_file.close()   
    for i in path_list:
        try:
            data = data[i]
        except KeyError:
            return KeyError
    return data 

def show(cmds):
    if len(cmds) > 2:
        if cmds[2] == "user" or cmds[2] == "user/username" or cmds[2] == "user/password":
            return LOG.error("No access to username and password!")
    elif len(cmds) == 2:
        data = _load()
        del data['user']
        return data
    path = ""
    data = _find_value(cmds[2])
    if data == KeyError:
        return ConfErrors.no_key(path)
    else:
        return LOG.info("{}".format(data))

def change(cmds):
    try:
        if not len(cmds) > 3:
            return "Missing Argument(s)!"
        path = cmds[2]
        
        path_list = path.split('/')
        
        data = _find_value(path)
        if data == KeyError:
            return ConfErrors.no_key(path)
        elif type(data) == dict:
            return ConfErrors.key_not_refer_str(path)
        
        private = False
        if cmds[2] == 'user/password':
            private = True
            if cmds[3] != data:
                return LOG.error('Please enter current password before change!')+LOG.info('\nUsage ->\nconf change user/password [CURRENT_PASSWORD] [NEW_PASSWORD]')
        elif cmds[2] == 'user/username':
            private = True
            if cmds[3] != _find_value('user/password'):
                return LOG.error('Please enter current password before change!')+LOG.info('\nUsage ->\nconf change user/username [CURRENT_USERNAME] [NEW_USERNAME]')
                
        config_file = open('//etc/config/configures.txt','r')
        global globaldata
        globaldata = json.loads(config_file.read())
        config_file.close()    
        
        if private:
            new_val = cmds[4]
        else:
            new_val = cmds[3]
        
        code_str = "globaldata"
        for path in path_list:
            code_str += "['{}']".format(path)
        code_str += "='{}'".format(new_val)
        exec(code_str)
        config_file = open('//etc/config/configures.txt','w',encoding="utf-8")
        json.dump(globaldata, config_file)
        config_file.close()
        return LOG.debug('The value which refers to "{}" successfully changed as "{}"'.format('/'.join(path_list),new_val))
    except Exception as ex:
        message = LOG.error("Configures can not be changed") + "\n"
        message += LOG.error("{}".format(ex))
        return message
