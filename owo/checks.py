import mimetypes
import json
from functools import lru_cache

CONFIG_URL = "https://raw.githubusercontent.com/whats-this/api/master/config.json"

__all__ = ["get_config","async_get_config",
           "check", "check_file", "async_check_file"]

@lru_cache()
def get_config():
    import requests
    response = requests.get(CONFIG_URL)
    if response.status_code != 200:
        raise ValueError("Expected 200, got {}\n{}".format(
            response.status_code, response.text))

    return json.dumps(response.json())
        
@lru_cache()
async def async_get_config(loop):
    import aiohttp
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(CONFIG_URL) as response:
            if response.status_code != 200:
                raise ValueError("Expected 200, got {}\n{}".format(
                    response.status_code, response.text))
                return json.dumps(await response.json())

@lru_cache()
def check(config, file):
    config = json.loads(config) # Cache requires `config` to be hashable
    if mimetypes.guess_type(file) == "text/plain":
        if file.split(".")[-1] not in config.get("textPlainExtensions"):
            raise ValueError("File extension {} not in allowed extensions.".format(
                file.split(".")[-1]))

    elif mimetypes.guess_type(file)[0] not in config.get("allowedFileTypes"):
        raise ValueError("File mimetype {} not in allowed mimetypes.".format(
            mimetypes.guess_type(file)[0]))

    return True

@lru_cache()
def check_file(file):
    config = get_config()
    return check(config, file)

@lru_cache()
async def async_check_file(file, loop):
    config = await async_get_config()
    return check(owo_config, file)