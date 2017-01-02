import mimetypes
import os.path
import sys

from functools import lru_cache

PY_VERSION = sys.version_info.major

__all__ = ["upload_files", "shorten_urls",
           "async_upload_files", "async_shorten_urls",
           "Client"]

BASE_URL = "https://api.awau.moe"

UPLOAD_PATH = "/upload/pomf"
SHORTEN_PATH = "/shorten/polr"

UPLOAD_STANDARD = "https://owo.whats-th.is/"
SHORTEN_STANDARD = "https://uwu.whats-th.is/"

UPLOAD_BASES = ("https://owo.whats-th.is/", "https://i.am-a.ninja/",
                "https://buttsare.sexy/", "https://nyanyanya.moe/",
                "https://all.foxgirlsare.sexy/", "https://i.stole-a-me.me/",
                "https://can-i-ask-dean-on-a.date/", "https://this.is-a.dog/",
				"https://deanis.sexy/")

SHORTEN_BASES = ("https://awau.moe/", "https://uwu.whats-th.is/")


def check_size(file):
    if os.path.getsize(file) > 83886080:
        raise OverflowError("File exceeds file size limit")


@lru_cache()
def upload_files(key: str, *files: str, verbose=False):
    try:
        import requests
    except ImportError:
        raise ImportError("Please install the `requests` module "
                          "to use this function")

    for file in files:
        check_size(file)

    multipart = [(
        "files[]",
        (
            file,
            open(file, "rb"),
            mimetypes.guess_type(file)[0]
        ))
        for file in files]

    response = requests.post(BASE_URL+UPLOAD_PATH, files=multipart,
                             params={"key": key})

    if response.status_code != 200:
        raise ValueError("Expected 200, got {}\n{}".format(
            response.status_code, response.text))

    if verbose:
        results = {
            item["name"]: {
                base: base+item["url"]
                for base in UPLOAD_BASES
            }
            for item in response.json()["files"]
        }

    else:
        results = {
            item["name"]: UPLOAD_STANDARD + item["url"]
            for item in response.json()["files"]
        }

    return results


@lru_cache()
def shorten_urls(key: str, *urls: str, verbose=False):
    try:
        import requests
    except ImportError:
        raise ImportError("Please install the `requests` module "
                          "to use this functio*n")

    # Make the request
    results = []

    for url in urls:
        response = requests.get(BASE_URL+SHORTEN_PATH,
                                params={"action": "shorten",
                                        "url": url,
                                        "key": key})

        if response.status_code != 200:
            raise ValueError("Expected 200, got {}\n{}".format(
                response.status_code, response.text))

        path = response.text.split("/")[-1]
        if verbose:
            results.append({
                base: base+path
                for base in SHORTEN_BASES
            })
        else:
            results.append(SHORTEN_STANDARD + path)

    return results


if PY_VERSION == 3:
    import asyncio

    @lru_cache()
    @asyncio.coroutine
    def async_upload_files(key: str, *files: str, loop=None, verbose=False):
        try:
            from . import aiohttp2
            import aiohttp
        except ImportError:
            raise ImportError("Please install the `aiohttp` module "
                              "to use this function")

        results = {}

        for file in files:
            check_size(file)

        with aiohttp2.MultipartWriter('form-data') as mp:
            for file in files:
                part = mp.append(open(file, "rb"))
                part.set_content_disposition(
                    'form-data',
                    should_quote=False,
                    name='files[]',
                    filename=file
                )

            with aiohttp.ClientSession(loop=loop) as session:
                with (
                    yield from session.post(BASE_URL+UPLOAD_PATH, data=mp,
                                            params={"key": key})) as response:
                    if response.status != 200:
                        raise ValueError("Expected 200, got {}\n{}".format(
                            response.status, (yield from response.text())))

                    for item in (yield from response.json())["files"]:
                        if item.get("error") is True:
                            raise ValueError("Expected 200, got {}\n{}".format(
                                item["errorcode"], item["description"]))

                        if verbose:
                            results[item["name"]] = {
                                base: base+item["url"]
                                for base in UPLOAD_BASES
                            }

                        else:
                            results[item["name"]] = UPLOAD_STANDARD+item["url"]

        return results

    @lru_cache()
    @asyncio.coroutine
    def async_shorten_urls(key: str, *urls: str, loop=None, verbose=False):
        try:
            import aiohttp
        except ImportError:
            raise ImportError("Please install the `aiohttp` module "
                              "to use this function")

        results = []

        with aiohttp.ClientSession(loop=loop) as session:
            for url in urls:
                with (
                    yield from session.get(BASE_URL+SHORTEN_PATH,
                                           params={"action": "shorten",
                                                   "url": url,
                                                   "key": key})) as response:
                    if response.status != 200:
                        raise ValueError("Expected 200, got {}\n{}".format(
                            response.status, (yield from response.text())))

                path = (yield from response.text()).split("/")[-1]
                if verbose:
                    results.append({
                        base: base+path
                        for base in SHORTEN_BASES
                    })
                else:
                    results.append(SHORTEN_STANDARD + path)

        return results


class Client:
    """
    In case you want to make multiple requests
    without constantly passing `api_key` and/or `loop`
    """

    def __init__(self, api_key: str, loop=None, verbose=False):
        self.key = api_key
        self.loop = loop
        self.verbose = verbose

    def toggle_verbose(self):
        self.verbose = not self.verbose

    def upload_files(self, *files: str):
        return upload_files(self.key, *files, verbose=self.verbose)

    def shorten_urls(self, *urls: str):
        return shorten_urls(self.key, *urls, verbose=self.verbose)

    if PY_VERSION == 3:
        @asyncio.coroutine
        def async_upload_files(self, *files: str):
            return async_upload_files(self.key, *files,
                                      loop=self.loop, verbose=self.verbose)

        @asyncio.coroutine
        def async_shorten_urls(self, *urls: str):
            return async_shorten_urls(self.key, *urls,
                                      loop=self.loop, verbose=self.verbose)
