import asyncio
import io
import mimetypes
import os.path as osp

from .utils import check_size, BASE_URL, MAX_FILES,\
    UPLOAD_PATH, SHORTEN_PATH, UPLOAD_STANDARD,\
    SHORTEN_STANDARD, UPLOAD_BASES, SHORTEN_BASES, headers


@asyncio.coroutine
def async_upload_files(key, *files, **kwargs):
    verbose = kwargs.get("verbose", False)
    loop = kwargs.get("loop", None)

    if len(files) > MAX_FILES:
        raise OverflowError("Maximum amout of files to send at once"
                            "is {}".format(MAX_FILES))

    try:
        import aiohttp
    except ImportError:
        raise ImportError("Please install the `aiohttp` module "
                          "to use this function")

    results = {}

    for file in files:
        if not isinstance(file, (str, bytes, io.IOBase)):
            raise ValueError("`file` should either be a `str`, `bytes` or an"
                             "inheriter of `io.IOBase` (open(), BytesIO,"
                             "etc.).")

        check_size(file)

    with aiohttp.MultipartWriter('form-data') as mp:
        for i, file in enumerate(files):
            if isinstance(file, str):
                # If string, read file
                data = open(file, "rb")
                name = file
            else:
                data = file
                name = getattr(file, "name", "file_{}".format(i))

            # Get only the filename, with no path.
            # Without this, attempting to upload files like `./foo.ext`
            # (with any path stuff, `./`, `dir/`, etc) will result in an
            # annoying error saying that there were no `files[]`.
            name = osp.basename(name).lower()

            part = mp.append(data, {'Content-Type':
                                    mimetypes.guess_type(name)[0] or
                                    'application/octet-stream'})
            part.set_content_disposition(
                'form-data',
                quote_fields=False,
                name='files[]',
                filename=name
            )

        session = aiohttp.ClientSession(loop=loop)
        response = yield from session.post(BASE_URL+UPLOAD_PATH, data=mp,
                                           params={"key": key},
                                           headers=headers)
        if response.status != 200:
            raise ValueError("Expected 200, got {}\n{}".format(
                response.status, (yield from response.text())))

        for item in (yield from response.json())["files"]:
            if item.get("error") is True:
                raise ValueError("Expected 200, got {}\n{}".format(
                    item["errorcode"], item["description"]))

            if verbose:
                results[item["name"]] = {
                    base: base+item["url"]
                    for base in UPLOAD_BASES
                }

            else:
                results[item["name"]] = UPLOAD_STANDARD+item["url"]

    return results


@asyncio.coroutine
def async_shorten_urls(key, *urls, **kwargs):
    verbose = kwargs.get("verbose", False)
    loop = kwargs.get("loop", None)

    try:
        import aiohttp
    except ImportError:
        raise ImportError("Please install the `aiohttp` module "
                          "to use this function")

    results = []

    session = aiohttp.ClientSession(loop=loop)
    for url in urls:
        response = yield from session.get(BASE_URL+SHORTEN_PATH,
                                          params={"action": "shorten",
                                                  "url": url,
                                                  "key": key},
                                          headers=headers)
        if response.status != 200:
            raise ValueError("Expected 200, got {}\n{}".format(
                response.status, (yield from response.text())))

        path = (yield from response.text()).split("/")[-1]
        if verbose:
            results.append({
                base: base+path
                for base in SHORTEN_BASES
            })
        else:
            results.append(SHORTEN_STANDARD + path)

    return results


class Client:
    @asyncio.coroutine
    def async_upload_files(self, *files):
        return async_upload_files(self.key, *files,
                                  loop=self.loop, verbose=self.verbose)

    @asyncio.coroutine
    def async_shorten_urls(self, *urls):
        return async_shorten_urls(self.key, *urls,
                                  loop=self.loop, verbose=self.verbose)
