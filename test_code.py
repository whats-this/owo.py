import asyncio
import os

import owo


key = os.environ.get("TRAVIS_KEY") or "1ae1c6d8-cc48-4fc4-8724-52b8f85d9847"
loop = asyncio.get_event_loop()


def test_upload():
    fname = owo.upload_files(key, "owo-logo.png")
    print(fname)


def test_shorten():
    hlink = owo.shorten_urls(key, "https://google.com")
    print(hlink)

# TODO: add more test cases
