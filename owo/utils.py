from collections import namedtuple
import os
import os.path

import requests

DOMAINS_URL = ("https://raw.githubusercontent.com/whats-this/landing/"
               "master/public-cdn-domains.txt")

resp = requests.get(DOMAINS_URL)
content = resp.text

version = "2.3.0"

headers = {
    "User-Agent": ("WhatsThisClient (https://github.com/whats-this/owo.py,"
                   f" {version}),")}

File = namedtuple("File", ["data", "name"])

MAX_FILES = 3
MAX_SIZE = 83889080

BASE_URL = "https://api.awau.moe"

UPLOAD_PATH = "/upload/pomf"
SHORTEN_PATH = "/shorten/polr"

UPLOAD_STANDARD = "https://owo.whats-th.is/"
SHORTEN_STANDARD = "https://uwu.whats-th.is/"

UPLOAD_BASES = ["https://{}/".format(url.split(":")[-1]) for url in
                content.split("\n")
                if "#" not in url]

SHORTEN_BASES = UPLOAD_BASES


def check_size(file):
    if isinstance(file, str):
        check = os.path.getsize(file) > MAX_SIZE
    elif isinstance(file.data, bytes):
        check = len(file.data) > MAX_SIZE
    else:
        # Should work for just about any file-like object (`open`, BytesIO, etc)
        # without consuming it.
        f = file.data
        old_pos = f.tell()

        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(old_pos, os.SEEK_SET)

        check = size > MAX_SIZE

    if check:
        raise OverflowError("File exceeds file size limit")
