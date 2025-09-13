import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import os

url = "https://summer.skyfall.dev/api/shop"

response = requests.get(url=url).json()
date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

os.makedirs(f"/home/olive/backup-bm-api/backups/{date}/images", exist_ok=True)
	

with open(f"/home/olive/backup-bm-api/backups/{date}/api.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

items = len(response)

for item in response:
	image_url = item["imageUrl"]
	response = requests.get(image_url, stream=True)
	path = urlparse(image_url).path
	ext = os.path.splitext(path)[1]
	id = item["id"]
	if response.status_code == 200:
		blocks = 0
		with open(f"/home/olive/backup-bm-api/backups/{date}/images/{id}{ext}", "wb") as img:
			for block in response.iter_content(chunk_size=8192):
				img.write(block)
				print("Wrote Block")
				blocks +=1
		print(f"Wrote {blocks} blocks from {id}")
		items -= 1
		print(f"{items} images left!")
	else:
		print(f"Failed to retrieve {id}, error code is {response.status_code}")
print(f"Wrote API to /home/olive/backup-bm-api/backups/{date}/api.json")
print(f"Wrote images to /home/olive/backup-bm-api/backups/{date}/images")


