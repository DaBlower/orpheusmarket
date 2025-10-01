import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import latest_backup

url = "https://summer.skyfall.dev/api/shop"

api_data = requests.get(url=url).json()

date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

try:
	print(f"{date} Checking if we need a backup")
	latest_backup_path = latest_backup.get_latest_backup()
	api_match = False
	img_match = False
	if latest_backup_path:
		with open(latest_backup_path, 'r') as back:
			latest_back = json.load(back)
			if json.dumps(latest_back, sort_keys=True) == json.dumps(api_data, sort_keys=True):
				print("nein")
				api_match = True
	else:
		# TODO: log error
		pass

	latest_images_path = latest_backup.get_latest_images()
	if latest_images_path:
		with open(latest_images_path, 'r') as img_json:
			latest_images = json.load(img_json)

		# remove date for fair comparison (the date will always be different lol)
		for key in latest_images:
			if 'date' in latest_images[key]:
				del latest_images[key]['date']

		# build expected new images
		expected_images = {}
		for item in api_data:
			image_url = item["imageUrl"]
			path = urlparse(image_url).path
			ext = os.path.splitext(path)[1]
			id = item["id"]
			expected_images[str(id)] = {
				"localImage": str(id) + ext,
				"remoteImage": image_url,
				"ext": ext
			}
		
		if json.dumps(latest_images, sort_keys=True) == json.dumps(expected_images, sort_keys=True):
			print("nein for img")
			img_match = True
		else:
			print("Images differ from previous backup")
	else:
		# TODO: log error
		pass
	if api_match and img_match:
		print(f"Both images and API match so we will skip the backup for {date}")
		# TODO: log matching so not making backup
		sys.exit(42)
	elif api_match:
		print(f"API matches but images differ so we will do a backup of everything anyways because obob is lazy :D")
	else:
		print("API or images differ so we will do a full backup")

except Exception as e:
	print(f"Failed to open api.json or images.json in previous backup at {latest_backup_path}")


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

image_path = os.path.join(project_root, "..", "static", "backups", date) # where images are stored
os.makedirs(image_path, exist_ok=True)

items = len(api_data)

images = {}

for item in api_data:
	image_url = item["imageUrl"]
	http_code = requests.get(image_url, stream=True)
	path = urlparse(image_url).path
	ext = os.path.splitext(path)[1]
	id = item["id"]
	if http_code.status_code == 200:
		blocks = 0
		image_name = str(id)+ext
		with open(os.path.join(image_path, image_name), "wb") as img:
			for block in http_code.iter_content(chunk_size=8192):
				img.write(block)
				print("Wrote Block")
				blocks +=1
		print(f"Wrote {blocks} blocks from {id}")
		items -= 1
		print(f"{items} images left!")
		images[str(id)] = {
			"localImage": image_name,
			"remoteImage": image_url,
			"date": date,
			"ext": ext
		}
	else:
		print(f"Failed to retrieve {id}, error code is {http_code.status_code}")
print(f"Wrote images to {image_path}")


with open(os.path.join(project_root, "..", "static", "backups", date, "api.json"), "w", encoding="utf-8") as f:
    json.dump(api_data, f, ensure_ascii=False, indent=4)

print(f'Wrote API to {os.path.join(project_root, "..", "static", "backups", date, "api.json")}')

src_folder = image_path

# dump image data
images_json_path = os.path.join(src_folder, "images.json")  # Fixed: Use dst_folder (static/backups/{date})
try:
    with open(images_json_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"Failed to write images.json: {e}")
