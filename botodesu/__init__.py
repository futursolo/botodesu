#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2017 Kaede Hoshikawa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Optional, Any, List

from . import _version
from ._version import *

from . import dikuto
from .dikuto import *

from . import exceptions
from .exceptions import *

from . import methods

from . import body
from .body import *

import asyncio
import aiohttp  # type: ignore
import re
import json
import functools
import warnings
import random
import traceback

__all__ = ["Boto"] + \
    _version.__all__ + dikuto.__all__ + exceptions.__all__ + body.__all__

_DEFAULT_BASE_URL = "https://api.telegram.org/bot{token}/{method}"

_USER_AGENT = "aiohttp/{} botodesu/{}".format(aiohttp.__version__, version)


class Boto:
    """
    Bo-to Desu!

    This is an automatically expand class.

    This class will expand its methods automatically.

    After using, the caller of this class should await its `_close` method or
    wrap it under an `async with` statement to perform automatic clean up when
    leaving the context.

    The long pulling method of getting updates is support through `async for`.

    See the example in the documentation.
    """
    def __init__(
        self, token: str, *, base_url: str=_DEFAULT_BASE_URL,
            loop: Optional[asyncio.AbstractEventLoop]=None) -> None:
        self._loop = loop or asyncio.get_event_loop()

        self._token = token
        self._base_url = base_url

        self._client = aiohttp.ClientSession(loop=self._loop)

        self._err_times = 0
        self._pending_updates = []  # type: List[dikuto.BotoDikuto]
        self._update_offset = 0

    def _make_request_url(self, method_name: str) -> str:
        return self._base_url.format(
            token=self._token, method=methods.get_url_name(method_name))

    async def _send_anything(
            self, __method_name: str, **kwargs: Any) -> Any:
        assert self._client is not None, "Boto is closed!"

        url = self._make_request_url(__method_name)

        # Telegram will cut off requests longer than 60 seconds,
        # but it's better to wait the server close the connection first.
        headers = {"User-Agent": _USER_AGENT}
        body_headers, data = body.generate(**kwargs)

        headers.update(body_headers)

        async with self._client.post(
                url, headers=headers, data=data, timeout=61) as response:
            content_text = await response.text()
            content = json.loads(
                content_text, object_pairs_hook=BotoDikuto)

            if response.status != 200:
                raise BotoEra(
                    "Era occurred when talking with the server.",
                    status_code=response.status,
                    content=content)

        if "ok" not in content.keys() or not content.ok:
            err_msg = "The server responded with an error."

            if "description" in content.keys():
                err_msg += " The server said: {}".format(content.description)

            raise BotoEra(
                err_msg, status_code=response.status, content=content)

        return content.result

    def __getattr__(self, name: str) -> Any:
        return functools.partial(self._send_anything, name)

    async def __aenter__(self) -> "Boto":
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self._close()

    async def __aiter__(self) -> "Boto":
        return self

    async def __anext__(self) -> dikuto.BotoDikuto:
        while (not self._pending_updates):
            try:
                updates = await self.get_updates(
                    limit=(random.random() * 40 + 10),
                    offset=self._update_offset,
                    timeout=55)
                # Fetch multiple updates(between 10 and 50) requests
                # at the same time.

                self._pending_updates.extend(updates)

            except:
                await asyncio.sleep((random.random() * 5 + 5))
                # Wait a peroid (between 5 and 10 sec) of time
                # before retrying.

                self._err_times += 1

                # If get_updates continuously errored more than 100
                # times, raise the error. This gives your `boto`
                # redundancy to bad network environments.
                if self._err_times >= 100:
                    self._err_times = 0
                    raise

            else:
                self._err_times = 0

        update = self._pending_updates.pop(0)
        self._update_offset = update.update_id + 1

        return update

    async def _close(self) -> None:
        """
        Clean up the Boto.
        """
        if self._update_offset != 0:
            try:  # Flush out the processed offset with a short poll.
                await self.get_updates(
                    limit=0,
                    offset=self._update_offset,
                    timeout=0)

            except:  # Failed to short poll.
                warnings.warn(
                    ("Boto cannot upload the offset to the telegram server,"
                     "the same update may be processed twice "
                     "on the next start, the actual offset is {}.\n{}").format(
                        self._update_offset, traceback.format_exc()),
                    BotoWarning)

        await self._client.close()
        self._client = None

    def __del__(self) -> None:
        if self._client is not None:
            warnings.warn(
                "Boto is not properly closed. "
                "Await `Boto._close()` or wrap it under an "
                "`async with` statement before it's been garbage collected.",
                BotoWarning)
