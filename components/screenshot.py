import os, pyautogui
from datetime import datetime
def take_screenshot():
    media_dir=os.path.join(os.getenv('APPDATA'),'vault','media')
    if not os.path.exists(media_dir):os.makedirs(media_dir)
    timestamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path=os.path.join(media_dir,f'screenshot_{timestamp}.png')
    pyautogui.screenshot(screenshot_path)