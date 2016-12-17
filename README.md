# OwO.whats-th.is wrapper for python

Installation:

Step 1: Get an API key
Step 2: `pip install http://github.com/whats-this/owo.py/archive/master.zip`


Usage:

```python

>>> import owo
>>> owo.shorten_urls(API_KEY, "url1","url2")
["shortened url 1","shortened url 2"]

>>> owo.upload_files(API_KEY, "file.png", "file.py")
{"file.png": "url", "file.py": "url"}

>>> import asyncio
>>> loop = asyncio.get_event_loop()
>>> loop.run_until_complete(
...     owo.async_shorten_urls(API_KEY, "url1","url2", loop=loop)
... )
...
["shortened url 1","shortened url 2"]

>>> loop.run_until_complete(
...     owo.async_upload_files(API_KEY, "file.png", "file.py", loop=loop)
... )
...
{"file.png": "url", "file.py": "url"}

```

If you don't want to pass around `api_key` and/or `loop`, use the `Client` class.

```python

>>> import owo
>>> my_client = owo.Client(API_KEY)
>>> my_client.shorten_urls("url1","url2")
["shortened url 1","shortened url 2"]

>>> my_client.upload_files("file.png", "file.py")
{"file.png": "url", "file.py": "url"}

>>> import asyncio
>>> loop = asyncio.get_event_loop()
>>> my_client = owo.Client(API_KEY, loop=loop)
>>> loop.run_until_complete(
...     my_client.async_shorten_urls("url1","url2")
... )
...
["shortened url 1","shortened url 2"]

>>> loop.run_until_complete(
...     my_client.async_upload_files("file.png", "file.py")
... )
...
{"file.png": "url", "file.py": "url"}

```