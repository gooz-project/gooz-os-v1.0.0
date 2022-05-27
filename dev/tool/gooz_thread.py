import os
import _thread
import utime
import gc
from wifuxlogger import WifuxLogger as LOG

flags = {}
thread_list=[]

class Usage():
    message = ""
    @staticmethod
    def start_usage():
        message += LOG.info('Usage -> thread start [PYTHON_FILE_NAME] --loop [LOOP_COUNT] --delay [SLEEP_TIME]')+'\n'
        message += LOG.info('[PYTHON_FILE_NAME] must be a ".py" file')+'\n'
        message += LOG.info('It will run python file [LOOP_COUNT] times')+'\n'
        message += LOG.info('[LOOP_COUNT] is not necessary, Default value :-1\nThat means it will run file until stopped manually')+'\n'
        message += LOG.info('[SLEEP_TIME] is not necessary, Default value :1')
        return message
    @staticmethod
    def stop_usage():
        message +=LOG.info('Usage -> thread stop [THREAD_ID]')
        return message
    @staticmethod
    def show_usage():
        message +=LOG.info('Usage -> thread show')+'\n'
        message +=LOG.info('It will shows current thread operations')
        return message
    @staticmethod
    def file_name_error(file_name):
        message +=LOG.info('There is no python file named {}!'.format(file_name))
        return message
    
def run(cmds):
    return eval('{}({})'.format(cmds[1],cmds))
    
def help(cmds): #pin gpio help
    command_list = ['stop','start','show']
    message = ""
    if not len(cmds) > 2:
        for command in command_list:
            message += command+'\n'
        return 'Commands: \n'+message+'\nFor more information about commands -> thread help [COMMAND_NAME]'
    try:
        return eval('Usage.{}_usage()'.format(cmds[2]))
    except:
        return LOG.error('There is no thread help for "{}"!'.format(cmds[2]))
        
def _gooz_script_thread(ID,code,delay = 1,loop = -1):
    while flags[ID]:
        if loop < 0:
            pass
        elif loop > 0:
            loop -= 1
        elif loop == 0:
            break
        exec(code)
        utime.sleep(delay)
    _delete_thread(ID)
 
def _gooz_function_thread(ID, target = None, args=(),loop=-1,delay=1):
    while flags[ID]:
        if loop < 0:
            pass
        elif loop > 0:
            loop -= 1
        elif loop == 0:
            break
        target(*args)
        utime.sleep(float(delay))
    _delete_thread(ID)
        
def _gooz_start_function_thread(target=None,args=(),thread_config={}):
    gc.collect()
    ID = _take_empty_ID()
    flags[ID] = True
    if not 'delay' in thread_config.keys():
        thread_config['delay'] = 1
    if not 'loop' in thread_config.keys():
        thread_config['loop'] = -1
    _thread.start_new_thread(_gooz_function_thread,(ID, target, args, int(thread_config['loop']),float(thread_config['delay'])))
    thread_config['ID'] = ID
    thread_list.append(thread_config)

def _take_empty_ID():
    ID = 1
    while ID in flags.keys():
        ID += 1
    return ID

def _delete_thread(ID):
    del flags[ID]
    for i in range(0,len(thread_list)):
        if thread_list[i]['ID'] == ID:
            del thread_list[i]
            break

def _take_code(code_file_name):
    try:
        with open(code_file_name, 'r') as f:
            code = f.read()
        return code
    except OSError:
        return False
        
def show(cmds):
    message = ""
    for i in thread_list:
        message += str(i)+'\n'
    return message.rstrip()
    
def stop(cmds):
    flags[int(cmds[2])] = False
    return "Thread with id {} is closed succesfully!".format(int(cmds[2]))
    
def start(cmds):
    gc.collect()
    if not len(cmds)>2:
        return LOG.error('Missing Argument(s)')+'\n'+LOG.info('Please use "thread help start" command for usage')
    code_file_name = cmds[2]
    code = _take_code(code_file_name)
    if code:
        ID = _take_empty_ID()
        flags[ID] = True
        thread_config = {'ID':ID,'type':'code','code_file_name':code_file_name,'--loop':'-1','--delay':'1'}
        from engine.gooz_engine import EngineTemplate
        EngineTemplate.parameter_parser(cmds,thread_config)
        _thread.start_new_thread(_gooz_script_thread,(ID,code,float(thread_config['--delay']),int(thread_config['--loop'])))
        thread_list.append(thread_config)
        return LOG.info("Thread is started succesfully")
    else:
        return Usage.file_name_error(code_file_name)
        
