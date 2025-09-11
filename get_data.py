import requests
import json

url = "https://summer.skyfall.dev/api/shop" # this is @mahad's api - if it breaks, i might make my own


def get_data():
    try:
        response_og = requests.get(url=url)
    except Exception as e:
        print(f"Failed to contact api: {e}")
    try:
        response = response_og.json()
    except requests.exceptions.JSONDecodeError:
        print(f"JSON decode error!")

    BM_ITEMS = []
    
    backup_warning = False

    if response_og.status_code == 503:
         with open("backup.json", 'r') as backup:
            all = json.load(backup)
            backup_warning = True
            for item in all:
                if item["isBlackMarket"] == True:
                    BM_ITEMS.append(item)

    else:
        for item in response:
            if item["isBlackMarket"] == True:
                    BM_ITEMS.append(item)

    return BM_ITEMS, backup_warning