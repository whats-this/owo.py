import os.path

MAX_FILES = 3

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
