from wifuxlogger import WifuxLogger as LOG
print(LOG.info('GoozOs is starting...'))
from etc.config.core import _find_value, change
from engine.gooz_engine import GoozEngine
import main
import time, gc
from sys import exit

gc.enable()
    
try:
    username = _find_value('user/username')
    password = _find_value('user/password')
    if username == "" and password == "":
        try:
            register()
        except Exception as ex:
            print(ex)
    machine_name = _find_value('system/machine')
except:
    print(LOG.error('Error while getting settings from config!'))
    print(LOG.error('Please check etc/config/configures.txt'))
    
    
def register():
    print(LOG.info("Please set username and password"))
    new_username = input('Username: ')
    new_password = input('Password: ')
    GoozEngine.run("conf change user/username {}".format(new_username))
    GoozEngine.run("conf change user/password {}".format(new_password))
    global username
    username = new_username
    global password
    password = new_password
    
    
def login(username, password):
    usr = input("Username -> ")
    pswd = input("Password -> ")
    if password == pswd and username == usr:
        print(LOG.info("Welcome {}".format(username)))
        return True
    else:
        print(LOG.error("Access Denied"))
        exit()
        return False
    
    
def connect_wifi(ssid, password, try_num=1000):
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected():
            print(LOG.info('Wifi already connected.'))
            return
        wlans = wlan.scan()
        found = False
        for x in wlans:
            if x[0] == b'{}'.format(ssid):
                found = True
        if not found:
            print(LOG.error('\nWifi named {} not found'.format(ssid)))
            main.start(username,machine_name)
            return
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            for x in range(0,try_num):
                if not wlan.isconnected():
                    time.sleep(0.01)
                    pass
                else:
                    break
        if wlan.isconnected():
            print(LOG.info('Wifi Connected: {}').format(wlan.ifconfig()))
        else:
            print(LOG.error('Connection timeout!'))
    except Exception as ex:
        print(ex)
 
    
def run_boot_commands():
    try:
        f = open('//boot_commands.txt','r')
        commands = f.readlines()
        f.close()
        for com in commands:
            GoozEngine.run(com.rstrip('\r\n'))
    except:
        pass

if _find_value('system/auto_login') == "False":
    main.login_flag = login(username, password)
else:
    main.login_flag = True
    
if _find_value('wifi/auto_connect') == 'True':
    print(LOG.info('Waiting for wifi connection...'))
    connect_wifi(_find_value('wifi/last_wifi_ssid'),_find_value('wifi/last_wifi_password'))

if _find_value('client/auto_connect') == 'True':
    GoozEngine.run("client start --port {}".format(_find_value('client/port')))

run_boot_commands()  
main.start(username, machine_name)
