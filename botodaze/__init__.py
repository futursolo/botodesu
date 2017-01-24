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

from typing import Optional, Dict, Any, Union, Dict, List

from . import _version
from ._version import *

import asyncio
import aiohttp  # type: ignore
import re
import json
import functools
import threading
import mimetypes
import multidict  # type: ignore

__all__ = ["BotoDikuto", "BotoLisuto", "BotoEra", "BotoFile", "Botodaze"] + \
    _version.__all__

_DEFAULT_BASE_URL = "https://api.telegram.org/bot{token}/{method}"

_ALLOWED_NAME = re.compile(r"^[a-z]([a-z\_]+)?$")

_USER_AGENT = "aiohttp/{} botodaze/{}".format(aiohttp.__version__, version)


class BotoDikuto(dict):
    pass


class BotoLisuto(list):
    pass


class BotoEra(Exception):
    def __init__(
        self, *args: Any, status_code: Optional[int]=None,
        content: Optional[Union[dict, list, str, bytes]]=None,
            **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.status_code = status_code
        self.content = content


_GLOBAL_LOCK = threading.Lock()


class _BotoMethods(Dict[str, str]):
    def __getitem__(self, name: str) -> str:
        if name not in self.keys():
            with _GLOBAL_LOCK:
                if re.fullmatch(_ALLOWED_NAME, name) is None:
                    raise BotoEra(
                        ("Unacceptable API Method Name: {}, "
                         "r\"^[a-z]([a-z\_]+)?$\" is expected.").format(name))

                self[name] = name.strip().replace("_", "")

        return dict.__getitem__(self, name)


class BotoFile:
    def __init__(self, filename: str, content: bytes) -> None:
        self._filename = filename
        self._content = content

        self._content_type = mimetypes.guess_type(self._filename)[0]
        self._content_transfer_encoding = "binary"

    def set_content_type(self, content_type: str) -> None:
        self._content_type = content_type

    def set_content_transfer_encoding(self, new_cte: str) -> None:
        self._content_transfer_encoding = new_cte


def _generate_form_data(**kwargs: Union[str, BotoFile]) -> aiohttp.FormData:
    form_fata = aiohttp.FormData()

    for name, value in kwargs.items():
        if isinstance(value, BotoFile):
            form_fata.add_field(
                name, value._content,
                content_type=value._content_type,
                filename=value._filename,
                content_transfer_encoding=value._content_transfer_encoding)

        else:
            form_fata.add_field(name, value)

    return form_fata


class Botodaze:
    """
    Boto daze!
    """
    def __init__(
        self, token: str, *, base_url: str=_DEFAULT_BASE_URL,
            loop: Optional[asyncio.AbstractEventLoop]=None) -> None:
        self._loop = loop or asyncio.get_event_loop()

        self._token = token
        self._base_url = base_url

        self._api_methods = _BotoMethods()
        self._update_offset = 0

        self._client = aiohttp.ClientSession(loop=self._loop)

    def _make_request_url(self, method_name: str) -> str:
        return self._base_url.format(
            token=self._token, method=self._api_methods[method_name])

    async def _send_anything(
            self, __method_name: str, **kwargs: Union[str, BotoFile]) -> Any:
        url = self._make_request_url(__method_name)

        # Telegram will cut off requests longer than 60 seconds,
        # but it's better to wait the server close the connection first.
        async with self._client.post(
            url, headers={"User-Agent": _USER_AGENT},
                data=_generate_form_data(**kwargs), timeout=61) as response:
            if response.content_type.find("json") != -1:
                raise BotoEra(
                    "Era occurred when talking with the server.",
                    status_code=response.status,
                    content=(await response.read()))

            content = await response.json()

            if isinstance(content, dict):
                content = BotoDikuto(content)

            elif isinstance(content, list):
                content = BotoLisuto(content)

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

    async def get_updates(
        self, offset: Optional[Union[int, str]]=None,
        limit: Union[int, str]=10,
            timeout: Union[int, str]=45) -> List[Dict[str, Any]]:
        get_updates_fn = self.__getattr__("get_updates")

        if offset is None:
            offset = self._update_offset

        else:
            self._update_offset = int(offset)

        updates = await get_updates_fn(
            offset=str(offset), limit=str(limit), timeout=str(timeout))

        if len(updates) > 0:
            self._update_offset = updates[-1].update_id + 1

        return updates

    async def close(self) -> None:
        raise NotImplementedError

    def __del__(self) -> None:
        if self._client is not None:
            pass  # Log Error.
