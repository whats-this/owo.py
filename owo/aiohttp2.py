# This here is purely to override aiohttp's quoting system
# because it's shit and PR #916 has been open for about a year
# Thanks to Leovoel for helping me with this

from aiohttp.multipart import TOKEN
from aiohttp.hdrs import CONTENT_DISPOSITION
from urllib.parse import quote

import aiohttp


class BodyPartWriter(aiohttp.BodyPartWriter):
    def set_content_disposition(self, disposition_type,
                                should_quote=True, **params):
        if not disposition_type or not (TOKEN > set(disposition_type)):
            raise ValueError('bad content disposition type '
                             '{!r}'.format(disposition_type))
        value = disposition_type
        if params:
            lparams = []
            for key, val in params.items():
                if not key or not (TOKEN > set(key)):
                    raise ValueError('bad content disposition parameter '
                                     '{!r}={!r}'.format(key, val))
                qval = quote(val, '') if should_quote else val
                lparams.append((key, '"%s"' % qval))
                if key == 'filename':
                    lparams.append(('filename*', "utf-8''" + qval))
            value = '; '.join((value, '; '.join('='.join(pair)
                                                for pair in lparams)))
        self.headers[CONTENT_DISPOSITION] = value


class MultipartWriter(aiohttp.MultipartWriter):
    part_writer_cls = BodyPartWriter
