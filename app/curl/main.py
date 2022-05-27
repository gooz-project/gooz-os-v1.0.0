import urequests
import json
from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG

def run(cmds):
    try:
        exec("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

    except Exception as ex:
        LOG.error(ex)
def post(cmds):
    #response = urequests.post("http://jsonplaceholder.typicode.com/posts", data = "some dummy content")
    blueprint = EngineTemplate.parameter_parser(cmds)
    response = urequests.post(blueprint["--url"],data = blueprint["--data"])
    LOG.info(response.text)
    response.close()
def get(cmds):
    if not "--url" in cmds :
        try:
            response = urequests.get(cmds[1])
            LOG.info("")
            print(response.text)
        except Exception as ex:
            LOG.error("Content can not be received")
            LOG.error(ex)
    else:
        blueprint = EngineTemplate.parameter_parser(cmds)
        response = urequests.get(blueprint["--url"])

        try:
            print(blueprint["--save"])
        except Exception:
            blueprint["--save"] = "empty"

        LOG.info(blueprint)
        if blueprint["--save"] == "empty":
            LOG.info(response.text)
        else:
            if blueprint["--type"] == "text":
                with open("/app/curl/downloads/"+blueprint["--save"]+".txt", "w") as fp:
                    fp.write(response.text)
            elif blueprint["--type"] == "json":
                with open("/app/curl/downloads/"+blueprint["--save"]+".json", "w") as fp:
                    json.dump(response.text, fp)
            else:
                LOG.warning("unsupported type")
