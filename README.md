# owo.py

A wrapper that was written inside of Python that allows for you to upload images to the owo.whats-th.is and shorten URLs through uwu.whats-th.is. Allows for both methods through Async and Non-Async. Currently only supported inside of Python 3 (3.5+ recommended).

# Instructions

1. Gain a API key in order to be actually able to use the service.
2. Run the command `pip install http://github.com/whats-this/owo.py/archive/master.zip`.
3. Check the usage below to find some basic examples of how to use the script.

# Usage

Basic usage of the script is like so.

**Image Uploading**

```python
import owo
owo.upload_files(API_KEY, "file.png", "file.py")
```

returns something like..

```python
{"file.png": "url", "file.py": "url"}
```

**URL Shortening**

```python
import owo
owo.shorten_urls(API_KEY, "url1","url2")
```

returns something like..

```python
["shortened url 1","shortened url 2"]
```

For more powerful/better examples please check /examples/.

# Contribute

1. Fork repo.
2. Edit code.
3. Make a PR.
4. Submit said PR.

# License

A copy of the MIT license can be found in `LICENSE.md`.
