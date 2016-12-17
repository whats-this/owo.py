import owo

key = input("Please enter your API key: ")

res = owo.shorten_urls(key,"http://google.com")
print(res)

res = owo.upload_files(key, "test.png", "owo.py")
print(res)


import asyncio
loop = asyncio.get_event_loop()

res = loop.run_until_complete(owo.async_shorten_urls(key, "http://google.com", loop=loop))
print(res)

res = loop.run_until_complete(owo.async_upload_files(key, "test.png", loop=loop))
print(res)