import os.path
import re
import requests

DOMAINS_URL = ("https://raw.githubusercontent.com/whats-this/landing/"
               "master/public-cdn-domains.txt")

resp = requests.get(DOMAINS_URL)
content = resp.text

version = "2.3.0"

headers = {
    "User-Agent": ("WhatsThisClient (https://github.com/whats-this/owo.py,"
                   f" {version}),")}

MAX_FILES = 3

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
    if os.path.getsize(file) > 83886080:
        raise OverflowError("File exceeds file size limit")
