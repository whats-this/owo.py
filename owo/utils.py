import os
import os.path

version = "2.3.0"
DOMAINS_URL = ("https://raw.githubusercontent.com/whats-this/landing/"
               "master/public-cdn-domains.txt")

try:
    import requests
except ImportError:
    # Installing package, ignore
    UPLOAD_BASES = SHORTEN_BASES = []
else:
    resp = requests.get(DOMAINS_URL)
    content = resp.text
    UPLOAD_BASES = ["https://{}/".format(url.split(":")[-1]) for url in
                    content.split("\n")
                    if "#" not in url]

    SHORTEN_BASES = UPLOAD_BASES

headers = {
    "User-Agent": ("WhatsThisClient (https://github.com/whats-this/owo.py,"
                   " {}),".format(version))}

MAX_FILES = 3
MAX_SIZE = 83889080

BASE_URL = "https://api.awau.moe"

UPLOAD_PATH = "/upload/pomf"
SHORTEN_PATH = "/shorten/polr"

UPLOAD_STANDARD = "https://owo.whats-th.is/"
SHORTEN_STANDARD = "https://uwu.whats-th.is/"


def check_size(file):
    if isinstance(file, str):
        check = os.path.getsize(file) > MAX_SIZE
    elif isinstance(file, bytes):
        check = len(file) > MAX_SIZE
    else:
        # Should work for just about any file-like object (`open`, BytesIO, etc)
        # without consuming it.
        old_pos = file.tell()

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(old_pos, os.SEEK_SET)

        check = size > MAX_SIZE

    if check:
        raise OverflowError("File exceeds file size limit")
