import requests

url = "https://summer.skyfall.dev/api/shop" # this is @mahad's api - if it breaks, i might make my own


def get_data():
    try:
        response = requests.get(url=url).json()
    except requests.exceptions.JSONDecodeError:
        print(f"JSON decode error!")
        return 5
    except Exception as e:
        print(f"Failed to contact api: {e}")
        return 6

    BM_ITEMS = []

    for item in response:
        if item["isBlackMarket"] == True:
                BM_ITEMS.append(item)

    return BM_ITEMS