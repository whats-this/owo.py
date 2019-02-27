#  _____ __ _____   _ __ _  _
# / _ \ V  V / _ \_| '_ \ || |
# \___/\_/\_/\___(_) .__/\_, |
#                  |_|   |__/
#
# USAGE EXAMPLES

# Required Imports
import owo

# Asynchronous Only Imports
import asyncio

# Optional Import for Making a Byte Stream
from io import BytesIO

# ############################################################

key = input("Please enter your API key: ")

# Upload Image
res = owo.upload_files(key, "example.png")
print(res)

# Shorten URL
res = owo.shorten_urls(key, "http://google.com")
print(res)

# ############################################################

loop = asyncio.get_event_loop()

# Upload Image
res = loop.run_until_complete(owo.async_upload_files(key,
                                                     "example.png",
                                                     loop=loop))
print(res)

# Shorten URL
res = loop.run_until_complete(owo.async_shorten_urls(key,
                                                     "http://google.com",
                                                     loop=loop))
print(res)

# ############################################################

# Upload Image from Memory
f = open("./example.png", "rb")

res = owo.upload_files(key, owo.File(f, "owologo.png"))
res2 = owo.upload_files(key, owo.File(BytesIO(b"this is my very cool file",
                                              "file.txt")))

print(res)
print(res2)

# Upload Image from Memory (Async)

loop = asyncio.get_event_loop()
f = open("./example.png", "rb")

res = loop.run_until_complete(owo.async_upload_files(key, owo.File(f,
                                                          "owologo.png")))
res2 = loop.run_until_complete(owo.async_upload_files(key, owo.File(BytesIO(
                                                           b"this is my very "
                                                           b"cool file",
                                                           "file.txt"))))

print(res)
print(res2)
