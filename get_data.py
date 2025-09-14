import requests
import json
import latest_backup

url = "https://summer.skyfall.dev/api/shop" # this is @mahad's api - if it breaks, i might make my own


def get_data(regular):
    try:
        response_og = requests.get(url=url)
    except Exception as e:
        print(f"Failed to contact api: {e}")
    try:
        response = response_og.json()
    except requests.exceptions.JSONDecodeError:
        print(f"JSON decode error!")

    items = []
    
    backup_warning = False

    if regular:
        shopType = "regular"
    else:
        shopType = "blackMarket"

    if response_og.status_code != 200:
        backup = latest_backup.get_latest_backup()
        if backup:
            with open(backup, 'r') as backup:
                all = json.load(backup)
                backup_warning = True
                for item in all:
                    if item["shopType"] == shopType:
                        items.append(item)

    else:
        for item in response:
            if item["shopType"] == shopType:
                    items.append(item)

    return items, backup_warning