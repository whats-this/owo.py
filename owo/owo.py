import mimetypes
import json
import base64
import io

__all__ = ["upload_files","shorten_urls","async_upload_files","async_shorten_urls","Client"]

BASE_URL = "https://api.whats-th.is"
IMAGE_PATH = "/upload/pomf"
URL_PATH = "/shorten/polr"
CONFIG_URL = "https://raw.githubusercontent.com/whats-this/api/master/config.json"

def check_file(file):
    try:
        owo_config
    except NameError:
        import requests
        response = requests.get(CONFIG_URL)
        if response.status_code != 200:
            raise ValueError("Expected 200, got {}\n{}".format(
                response.status_code, response.text))

        owo_config = response.json()

    if mimetypes.guess_type(file) == "text/plain":
        if file.split(".")[-1] not in owo_config.get("textPlainExtensions"):
            raise ValueError("File extension {} not in allowed extensions.".format(
                file.split(".")[-1]))

    elif mimetypes.guess_type(file)[0] not in owo_config.get("allowedFileTypes"):
        raise ValueError("File mimetype {} not in allowed mimetypes.".format(
            mimetypes.guess_type(file)[0]))

    return True

async def async_check_file(file, loop):
    try:
        owo_config
    except NameError:
        import aiohttp
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(CONFIG_URL) as response:
                if response.status_code != 200:
                    raise ValueError("Expected 200, got {}\n{}".format(
                        response.status_code, response.text))

                global owo_config
                owo_config = await response.json()

    if mimetypes.guess_type(file)[0] == "text/plain":
        if file.split(".")[-1] not in owo_config.get("textPlainExtensions"):
            raise ValueError("File extension {} not in allowed extensions.".format(
                file.split(".")[-1]))

    elif mimetypes.guess_type(file)[0] not in owo_config.get("allowedFileTypes"):
        raise ValueError("File mimetype {} not in allowed mimetypes.".format(
            mimetypes.guess_type(file)[0]))

    return True

def upload_files(key:str, *files: str):
    try:
        import requests
    except ImportError:
        raise ImportError("Please install the `requests` module to use this function")

    for file in files:
        check_file(file)

    multipart = [(
        "files[]",
        (
            file,
            open(file, "rb"),
            mimetypes.guess_type(file)[0]
        ))
        for file in files]

    response = requests.post(BASE_URL+IMAGE_PATH, files=multipart, params={"key":key})

    if response.status_code != 200:
        raise ValueError("Expected 200, got {}\n{}".format(
            response.status_code, response.text))

    return {item["name"]: "https://owo.whats-th.is/"+item["url"]
            for item in response.json()["files"]}

def shorten_urls(key:str, *urls:str):
    try:
        import requests
    except ImportError:
        raise ImportError("Please install the `requests` module to use this functio*n")

    # Make the request
    results = []

    for url in urls:
        response = requests.get(BASE_URL+URL_PATH, params={"action":"shorten","url":url, "key":key})

    if response.status_code != 200:
        raise ValueError("Expected 200, got {}\n{}".format(
            response.status_code, response.text))

    results.append(response.text)

    return results

async def async_upload_files(key:str, *files: str, loop=None):
    try:
        from . import aiohttp2
        import aiohttp
    except ImportError:
        raise ImportError("Please install the `aiohttp` module to use this function")

    results = {}
    
    for file in files:
        await async_check_file(file, loop)

    with aiohttp2.MultipartWriter('form-data') as mp:
        for file in files:
            part = mp.append(open(file, "rb"))
            part.set_content_disposition(
                'form-data',
                should_quote=False,
                name='files[]',
                filename=file
            )

        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post(BASE_URL+IMAGE_PATH, data=mp, params={"key":key}) as response:
                if response.status != 200:
                    raise ValueError("Expected 200, got {}\n{}".format(
                        response.status, await response.text()))

                for item in (await response.json())["files"]:
                    if item.get("error") is True:
                        raise ValueError("Expected 200, got {}\n{}".format(
                            item["errorcode"], item["description"]))

                    results[item["name"]] = "https://owo.whats-th.is/"+item["url"]

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
                    raise ValueError("Expected 200, got {}\n{}".format(
                        response.status, await response.text()))

            results.append(await response.text())

    return results

class Client:
    """
    In case you want to make multiple requests
    without constantly passing `api_key` and/or `loop`
    """

    def __init__(self, api_key:str, loop=None):
        self.key = api_key
        self.loop = loop

    def upload_files(self, *files: str):
        return upload_files(self.key, *files)

    def shorten_urls(self, *urls: str):
        return shorten_urls(self.key, *urls)

    async def async_upload_files(self, *files: str):
        return async_upload_files(self.key, *files, loop=self.loop)

    async def async_shorten_urls(self, *urls: str):
        return async_shorten_urls(self.key, *urls, loop=self.loop)
