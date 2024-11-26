import os, random, string
def confirmsend():
    os.makedirs(os.path.join(os.getenv('APPDATA'), 'vault'), exist_ok=True)
    with open(os.path.join(os.getenv('APPDATA'), 'vault', 'confirmation.fullbright'), 'w') as f:
        f.write(''.join(random.choices(string.ascii_letters + string.digits, k=6000)) + '\n\n')
        f.write('THIS FILE IS A CERTIFICATE CONFIRMING THAT THE VAULT FOLDER HAS BEEN FILLED AND IS READY TO SEND')