#  _____ __ _____   _ __ _  _
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/
#
# UPLOAD EXAMPLES

# ############################################################

# If you don't want to pass your key each time,
# define it within the Client class.

import owo

API_KEY = input("Please enter your API key: ")

my_client = owo.Client(API_KEY)

# Then the following methods can be changed to..

my_client.upload_files("example.png", "example.txt")

# The client also stores verbosity (default: False), which can be toggled using
# Client.toggle_verbose()
# Verbosity should be given using a kwarg to __init__, i.e.

my_client = owo.Client(API_KEY, verbose=True)
my_client.toggle_verbose()
my_client.verbose  # False

# ############################################################

# NON ASYNCHRONOUS EXAMPLES

# Specify which files that you would like to upload.
owo.upload_files(API_KEY, "example.png", "example.txt")

# Example output: {"example.png": "url", "example.txt": "url"}

# It is also possible to toggle verbosity
owo.upload_files(API_KEY, "example.png", "example.txt", verbose=True)

# Example output:
# {
#     'example.png': {'base domain 1': 'url 1', 'base domain 2': 'other url 1'},
#     'example.txt': {'base domain 1': 'url 2', 'base domain 2': 'other url 2'}
# }

# ############################################################

# ASYNCHRONOUS EXAMPLES

import asyncio

loop = asyncio.get_event_loop()

loop.run_until_complete(
    owo.async_upload_files(API_KEY, "example.png", "example.txt", loop=loop))

# Example output: {"example.png": "url", "example.txt": "url"}

# ############################################################

# IN-MEMORY EXAMPLES

# You can also pass `upload_files` and `async_upload_files` a bytes object or
# an object that inherits from `io.IOBase`, which includes objects like files
# from `open()`, or `BytesIO`.

import io

owo.upload_files(API_KEY, open("./example.png", "rb"))

# Example output: {"example.png": "url"}

loop.run_until_complete(
    owo.async_upload_files(API_KEY, io.BytesIO(b"My very cool file"), loop=loop
                           ))

# Example output: {"file_0": "url"}

# If the object has a `name` property, that will be used as the filename
# passed when uploading, otherwiose it'll take its index and make its filename
# `file_i`, where 'i' is the index.

# Multiple unnamed objects

owo.upload_files(API_KEY, io.BytesIO(b"File one"), io.BytesIO(b"File two"))

# Example output: {"file_0": "url", "file_1": "url"}