from engine.engine_template import EngineTemplate
from wifuxlogger import WifuxLogger as LOG
from urequests import get as restget
from ujson import loads as jloads
import os

def run(cmds):
    print(LOG.debug("Exec"))
    return eval("{}({})".format(cmds[1],EngineTemplate.exec_formatter_api(cmds)))

def install(cmds):
    if ":" in cmds[2]:
        new = cmds[2].split(":")
    else:
        response = jloads(restget("https://raw.githubusercontent.com/gooz-project/gooz_packages/main/"+cmds[2]+"/default.json").text)
        os.mkdir("/app/" + response["name"])
        for codes in response["codes"]:
            with open("/app/" + str(response["name"]) + "/" + str(codes["filename"]), "w+", encoding='utf-8') as f:
                codes["code"] = codes["code"].replace("pkglineflag", "\n")
                f.write(str(codes["code"]))
                f.close()
        return LOG.debug("Install") + "\n" + LOG.info("Package has been created.")

def uninstall(cmds):
    try:
        files = os.listdir("/app/" + cmds[2])
        for i in files:
            os.remove("/app/" + cmds[2] + "/" + i)
        os.rmdir("/app/" + cmds[2])
        return LOG.info("Package has been deleted.")

    except Exception:
        return LOG.error("Package not found.")
