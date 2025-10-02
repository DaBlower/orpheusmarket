import requests
import json
import time
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse
import logging
import sys
import os

max_retries = 5 # for downloading images + api
retry_delay = 5 # seconds
max_workers = 10 # number of parallel downloads

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import latest_backup

date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(logs_dir, exist_ok=True)


log_filename = f"backup_{date}.log"
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.StreamHandler(), # log to console
		logging.FileHandler(os.path.join(logs_dir, log_filename))
	]
)

logger = logging.getLogger(__name__)

url = "https://summer.skyfall.dev/api/shop"

api_data = requests.get(url=url).json()

try:
	logger.info(f"{date} Checking if we need a backup")
	latest_backup_path = latest_backup.get_latest_backup()
	logger.info("Now doing API")
	logger.debug(f"latest_backup_path = {latest_backup_path}")
	api_match = False
	img_match = False
	if latest_backup_path:
		with open(latest_backup_path, 'r') as back:
			latest_back = json.load(back)
			if json.dumps(latest_back, sort_keys=True) == json.dumps(api_data, sort_keys=True):
				logger.info(f"The latest backup matches the api :D")
				api_match = True
			else:
				logger.info("API differs from previous backup")
	else:
		logger.error("latest_backup_path is None!")

	latest_images_path = latest_backup.get_latest_images()
	logger.info("Now doing images")
	logger.debug(f"latest_images_path is {latest_images_path}")
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
		
		logger.debug(f"Latest images\n{latest_images}")
		logger.debug(f"Expected images\n{expected_images}")

		if json.dumps(latest_images, sort_keys=True) == json.dumps(expected_images, sort_keys=True):
			logger.info("latest_images and expected_images are equal!")
			img_match = True
		else:
			logger.info("Images differ from previous backup")
	else:
		logger.error("latest_images_path is None!")

	if api_match and img_match:
		logger.info(f"Both images and API match so we will skip the backup for {date}")
		sys.exit(42)
	elif api_match:
		logger.info(f"API matches but images differ so we will do a backup of everything anyways because obob is lazy :D")
	else:
		logger.info("Images differ so we will do a full backup")

except Exception as e:
	logger.error(f"Failed to open api.json or images.json in previous backup at {latest_backup_path}, did your backup stop midway last run?: {e}")


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

image_path = os.path.abspath(os.path.join(project_root, "..", "static", "backups", date)) # where images are stored
os.makedirs(image_path, exist_ok=True)

items = len(api_data)

images = {}

def download_image(item, image_path, date):
	image_url = item["imageUrl"]
	path = urlparse(image_url).path
	ext = os.path.splitext(path)[1]
	id = item["id"]

	success = False
	for attempt in range(max_retries):
		try:
			http_code = requests.get(image_url, stream=True, timeout=20)
			if http_code.status_code == 200:
				blocks = 0
				image_name = str(id)+ext
				with open(os.path.join(image_path, image_name), "wb") as img:
					for block in http_code.iter_content(chunk_size=8192):
						img.write(block)
						logger.debug("Wrote Block")
						blocks +=1
				logger.info(f"Wrote {blocks} blocks from item {id}")
				result = {
					"id": str(id),
					"localImage": image_name,
					"remoteImage": image_url,
					"date": date,
					"ext": ext
				}
				success = True
				return result
			else:
				logger.error(f"Attempt {attempt + 1} failed for {id}, error code is {http_code.status_code}")
		except requests.RequestException as e:
			logger.error(f"Attempt {attempt + 1} failed for {id}: {e}")
	
		if attempt < max_retries - 1:
			logger.info(f"Retrying {id} in {retry_delay} seconds...")
			time.sleep(retry_delay)
	if not success:
		logger.error(f"Failed to retrieve {id} after {max_retries} attempts. Skipping.")
		return None

logger.info(f"Starting parallel downloads with {max_workers} workers")
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
	futures = [executor.submit(download_image, item, image_path, date) for item in api_data]

	completed = 0
	for future in concurrent.futures.as_completed(futures):
		result = future.result()
		if result:
			images[result["id"]] = result
		else:
			logger.error(f"Download failed for an item")
		completed += 1
		logger.info(f"{len(api_data) - completed} images left!")

logger.info(f"Wrote images to {image_path}")


with open(os.path.join(project_root, "..", "static", "backups", date, "api.json"), "w", encoding="utf-8") as f:
    json.dump(api_data, f, ensure_ascii=False, indent=4)

logger.info(f'Wrote API to {os.path.abspath(os.path.join(project_root, "..", "static", "backups", date, "api.json"))}')

src_folder = image_path

# dump image data
images_json_path = os.path.abspath(os.path.join(src_folder, "images.json"))  # use dst_folder (static/backups/{date})
try:
    with open(images_json_path, "w", encoding="utf-8") as f:
        json.dump(images, f, ensure_ascii=False, indent=4)
    logger.info(f"Dumped images.json to {images_json_path}")
except Exception as e:
    logger.error(f"Failed to write images.json: {e}")