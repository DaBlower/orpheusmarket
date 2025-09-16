import requests
import json
import shutil
from datetime import datetime
from urllib.parse import urlparse
import os

url = "https://summer.skyfall.dev/api/shop"

api_data = requests.get(url=url).json()
date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

image_path = os.path.join(project_root, "backups", date, "images") # where images are stored
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
print(f"Wrote API to {os.path.join(project_root, 'api.json')}")
print(f"Wrote images to {image_path}")


with open(os.path.join(project_root, "backups", date, "api.json"), "w", encoding="utf-8") as f:
    json.dump(api_data, f, ensure_ascii=False, indent=4)

src_folder = image_path
dst_folder = os.path.abspath(os.path.join(project_root, "..", "static", "backups", date))

os.makedirs(dst_folder, exist_ok=True)

# save to static
for file_name in os.listdir(src_folder):
	src_file = os.path.join(src_folder, file_name)
	dst_file = os.path.join(dst_folder, file_name)
	if os.path.isfile(src_file):
		shutil.copy2(src_file, dst_file)
		print(f"Copied image from {src_file} to {dst_file}")

# dump image data
images_json_path = os.path.join(dst_folder, "images.json")  # Fixed: Use dst_folder (static/backups/{date})
try:
    with open(images_json_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"Failed to write images.json: {e}")


print(f"Copied contents from {src_folder} to {dst_folder}")