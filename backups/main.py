import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import os

url = "https://summer.skyfall.dev/api/shop"

response = requests.get(url=url).json()
date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

os.makedirs(os.path.join(project_root, "backups", date, "images"), exist_ok=True)

items = len(response)

for item in response:
	image_url = item["imageUrl"]
	response = requests.get(image_url, stream=True)
	path = urlparse(image_url).path
	ext = os.path.splitext(path)[1]
	id = item["id"]
	if response.status_code == 200:
		blocks = 0
		image_path = os.path.join(project_root, "backups", date, "images")
		with open(os.path.join(image_path, id+ext), "wb") as img:
			for block in response.iter_content(chunk_size=8192):
				img.write(block)
				print("Wrote Block")
				blocks +=1
		print(f"Wrote {blocks} blocks from {id}")
		items -= 1
		print(f"{items} images left!")
	else:
		print(f"Failed to retrieve {id}, error code is {response.status_code}")
	item["localUrl"] = id
print(f"Wrote API to {os.path.join(project_root, "api.json")}")
print(f"Wrote images to {image_path}")


with open(os.path.join(project_root, "api.json"), "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)