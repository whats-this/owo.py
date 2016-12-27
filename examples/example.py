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
                                                     "test.png",
                                                     loop=loop))
print(res)

# Shorten URL
res = loop.run_until_complete(owo.async_shorten_urls(key,
                                                     "http://google.com",
                                                     loop=loop))
print(res)
