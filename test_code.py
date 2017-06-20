import asyncio
import os

import owo


key = os.environ["TRAVIS_KEY"]
loop = asyncio.get_event_loop()


def test_upload():
    fname = owo.upload_files(key, "owo-logo.png")
    print(fname)


def test_shorten():
    hlink = owo.shorten_urls(key, "https://google.com")
    print(hlink)

# TODO: add more test cases
