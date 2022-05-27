from engine.engine_template import EngineTemplate
from engine.gooz_engine import GoozEngine
from wifuxlogger import WifuxLogger as LOG
from dev.wifi.core import sta_if
import socket
import ujson
import _thread
from etc.config.core import _find_value
from gc import collect
breakFlag = 1
client = None
address = None
flagger = 0
mainPageFlag = 1
cl = None

def run(cmds):
    try:
        global flagger
        for i in cmds:
            if "-d" in i or "--deattach" in i:
                flagger = 1
        if flagger:
            destart(cmds)
            flagger = 0
        else:
            return eval("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))
    except Exception as ex:
        return LOG.error(ex)
    return "OK"
        
def start_thread(cmds):
    _thread.start_new_thread(start, [cmds])
    return "start_thread OK"
    
def start(cmds):
    global cl
    global data_tx
    global breakFlag
    global client
    global address
    breakFlag = 1
    blueprint = EngineTemplate.parameter_parser(cmds)
    try:
        port = blueprint["--port"]
    except:
        if _find_value("client/port") == "":
            return LOG.warning("Please set a default port using 'conf change client/port [PORT]'")
        port = _find_value("client/port")
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', int(port)))
    s.listen(1)
    print(LOG.info("Client has started on {}:{} successfully.".format(sta_if.ifconfig()[0], port)))
    while breakFlag:
        cl, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        client = cl
        address = addr
        cl_file = cl.makefile('rwb', 0)
        line = str(cl.recv(1024*4),"utf-8")
        txData = line
        line = line.split("\n")
        
        myjson = txData.split("\r\n\r\n")[1]
        myjson = ujson.loads(myjson)
        data_tx = str(myjson["cmd"])
        request_type = line[0].split(" ")
        
        if request_type[0] == "POST":
            endpoints = request_type[1][1:].split("/")
            url_parser = ""
            for i in endpoints:
                url_parser += "."
                url_parser += i
            try:
                if "favicon" in url_parser:
                    pass
                else:
                    mainPage(data_tx)
            except Exception as ex:
                LOG.error(ex)
        cl.close()
        collect()
        del line, address, cl, addr, cl_file, txData, myjson
    return LOG.info("Client is closed.")

    
def mainPage(data):
    global client
    global mainPageFlag
    result = GoozEngine.run(data)
    if mainPageFlag == 0:
        mainPageFlag = 1
        return "CLOSED"
    client.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
    client.send(str(result))
    return "OK"


def close(cmds):
    global breakFlag
    global client
    global address
    global mainPageFlag
    try:
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
        client.send("Client is closed successfully.")
        client.close()
        breakFlag = 0
        mainPageFlag = 0
        del client
        return "OK"
    except:
        return LOG.error("Client couldn't be closed.")
