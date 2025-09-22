import requests
import json
import os
import latest_backup

url = "https://summer.skyfall.dev/api/shop" # this is @mahad's api - if it breaks, i might make my own


def get_data(regular, backup=None):

    items = []
    images = {}

    if regular:
        shopType = "regular"
    else:
        shopType = "blackMarket"

    if not backup:
        backup_warning = False
        try:
            response_og = requests.get(url=url)
            response = response_og.json()

            if response_og.status_code != 200:
                backup_warning = True
                backup = latest_backup.get_latest_backup()
                if backup:
                    with open(backup, 'r') as back:
                        all = json.load(back)
                        for item in all:
                            if item["shopType"] == shopType:
                                items.append(item)

            else:
                backup_warning = False
                for item in response:
                    if item["shopType"] == shopType:
                        items.append(item)   

        except requests.exceptions.JSONDecodeError:
            print(f"JSON decode error!")
            backup_warning = True
            backup = latest_backup.get_latest_backup()
            if backup:
                with open(backup, 'r') as back:
                    all = json.load(back)
                    for item in all:
                        if item["shopType"] == shopType:
                            items.append(item)

        except Exception as e:
            print(f"Failed to contact api: {e}")
            backup_warning = True
            backup = latest_backup.get_latest_backup()
            if backup:
                with open(backup, 'r') as back:
                    all = json.load(back)
                    for item in all:
                        if item["shopType"] == shopType:
                            items.append(item)


        images_d = latest_backup.get_latest_images()
        if images_d:
            with open(images_d, "r") as image_dict:
                images = json.load(image_dict)

    else:
        backup_warning = True
        images = {}

        
        try:
            with open(backup, "r") as f:
                all = json.load(f)
                backup_warning = True
                for item in all:
                    if item["shopType"] == shopType:
                        items.append(item)

        except Exception as e:
            print(f"Failed to open backup! {e}")

        try:
            with open(os.path.abspath(os.path.join(backup, "..", "images.json"))) as image_d:
                if image_d:
                    images = json.load(image_d)
        
        except Exception as e:
            print(f"Failed to load images! {e}")
            
    return items, backup_warning, images