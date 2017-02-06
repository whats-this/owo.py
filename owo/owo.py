import mimetypes
import sys

try:
    from functools import lru_cache
except ImportError:
    # python 2 doesnt have lru_cache
    # Create a dummy wrapper instead

    def lru_cache(maxsize=None):
        def wrapper(func):
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner
        return wrapper

from .utils import check_size, BASE_URL, MAX_FILES,\
    UPLOAD_PATH, SHORTEN_PATH, UPLOAD_STANDARD,\
    SHORTEN_STANDARD, UPLOAD_BASES, SHORTEN_BASES

PY_VERSION = sys.version_info.major

if PY_VERSION == 3:
    __all__ = ["upload_files", "shorten_urls",
               "async_upload_files", "async_shorten_urls",
               "Client"]
else:
    __all__ = ["upload_files", "shorten_urls",
               "Client"]


@lru_cache(maxsize=None)
def upload_files(key, *files, **kwargs):
    verbose = kwargs.get("verbose", False)
    if len(files) > MAX_FILES:
        raise OverflowError("Maximum amout of files to send at once"
                            "is {}".format(MAX_FILES))

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
            file.lower(),
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


@lru_cache(maxsize=None)
def shorten_urls(key, *urls, **kwargs):
    verbose = kwargs.get("verbose", False)
    try:
        import requests
    except ImportError:
        raise ImportError("Please install the `requests` module "
                          "to use this function")

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


class Client:
    """
    In case you want to make multiple requests
    without constantly passing `api_key` and/or `loop`
    """

    def __init__(self, api_key, **kwargs):
        self.key = api_key
        self.loop = kwargs.get("loop", None)
        self.verbose = kwargs.get("verbose", False)

    def toggle_verbose(self):
        self.verbose = not self.verbose

    def upload_files(self, *files):
        return upload_files(self.key, *files, verbose=self.verbose)

    def shorten_urls(self, *urls):
        return shorten_urls(self.key, *urls, verbose=self.verbose)


if PY_VERSION == 3:
    from . import async_owo

    class Client(async_owo.Client, Client):
        pass

    async_upload_files = async_owo.async_upload_files
    async_shorten_urls = async_owo.async_shorten_urls
