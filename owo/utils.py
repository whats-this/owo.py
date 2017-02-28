import os.path
import re

DOMAINS_URL = "https://raw.githubusercontent.com/whats-this/landing/master/public-cdn-domains.txt"

import requests
resp = requests.get(DOMAINS_URL)
content = resp.text

MAX_FILES = 3

BASE_URL = "https://api.awau.moe"

UPLOAD_PATH = "/upload/pomf"
SHORTEN_PATH = "/shorten/polr"

UPLOAD_STANDARD = "https://owo.whats-th.is/"
SHORTEN_STANDARD = "https://uwu.whats-th.is/"

UPLOAD_BASES = ["https://{}/".format(url) for url in re.findall("files:(.+)", content)]

SHORTEN_BASES = ["https://{}/".format(url) for url in re.findall("link:(.+)", content)]


def check_size(file):
    if os.path.getsize(file) > 83886080:
        raise OverflowError("File exceeds file size limit")
