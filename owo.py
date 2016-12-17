import mimetypes
import json
import base64
import io

__all__ = ["upload_file","shorten_url"]

BASE_URL = "https://api.whats-th.is"
IMAGE_PATH = "/upload/pomf"
URL_PATH = "/shorten/polr"

def upload_files(key:str, *files: str):
	try:
		import requests
	except ImportError:
		raise ImportError("Please install the `requests` module to use this function")
	
	multipart = [("files[]", (file, open(file, "rb"), mimetypes.guess_type(file)[0])) for file in files]
	
	response = requests.post(BASE_URL+IMAGE_PATH, files=multipart, params={"key":key})
		
	if response.status_code != 200:
		raise ValueError("Expected 200, got {}\n{}".format(response.status, response.text))

	return {item["name"]: "owo.whats-th.is/"+item["url"] for item in response.json()["files"]}

def shorten_urls(key:str, urls:str):
	try:
		import requests
	except ImportError:
		raise ImportError("Please install the `requests` module to use this function")
	
	# Make the request
	results = []
	
	for url in urls:
		response = requests.get(BASE_URL+URL_PATH, params={"action":"shorten","url":url, "key":key})
	
		if response.status_code != 200:
			raise ValueError("Expected 200, got {}\n{}".format(response.status, response.text))
		
		results.append(response.text)
		
	return results
	
async def async_upload_files(key:str, *files: str, loop=None):
	try:
		from . import aiohttp2
		import aiohttp
	except ImportError:
		raise ImportError("Please install the `aiohttp` module to use this function")
	
	results = {}
	
	with aiohttp2.MultipartWriter('form-data') as mp:
		for file in files:
			with open(file,"rb") as f:
				part = mp.append(io.BytesIO(f.read())) # Insert the files now so we don't get a `ValueError: read of closed file`
				part.set_content_disposition('form-data', should_quote=False, name='files[]', filename=file)
		async with aiohttp.ClientSession(loop=loop) as session:
			async with session.post(BASE_URL+IMAGE_PATH, data=mp, params={"key":key}) as response:
				if response.status != 200:
					raise ValueError("Expected 200, got {}\n{}".format(response.status, await response.text()))
				print(await response.text())
				#item = (await response.json())["files"]
				#results[item["name"]] = "owo.whats-th.is/"+item["url"]
			
	return results

async def async_shorten_urls(key:str, *urls:str, loop=None):
	try:
		import aiohttp
	except ImportError:
		raise ImportError("Please install the `aiohttp` module to use this function")
	
	results = []
	
	async with aiohttp.ClientSession(loop=loop) as session:
		for url in urls:
			async with session.get(BASE_URL+URL_PATH, params={"action":"shorten","url":url, "key":key}) as response:
				if response.status != 200:
					raise ValueError("Expected 200, got {}\n{}".format(response.status, await response.text()))
			results.append(await response.text())
		
	return results