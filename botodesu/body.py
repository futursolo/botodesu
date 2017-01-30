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

"""
Request Body Generation.
"""

from typing import Union, Any, Tuple, AnyStr, Dict

import aiohttp  # type: ignore
import mimetypes
import json

__all__ = ["BotoFairu"]


class BotoFairu:
    """
    Helper class for file uploading.

    The content type will be guessd by `mimetypes` depending on the file name.
    The default content transfer encoding is binary.

    These options can be overriden by using the methods below.
    """
    def __init__(self, filename: str, content: bytes) -> None:
        self._filename = filename
        self._content = content

        self._content_type = mimetypes.guess_type(self._filename)[0]
        self._content_transfer_encoding = "binary"

    def set_content_type(self, content_type: str) -> None:
        """
        Override the content type guessd by `mimetypes`.
        """
        self._content_type = content_type

    def set_content_transfer_encoding(self, new_cte: str) -> None:
        """
        Override the default content transfer encoding.
        """
        self._content_transfer_encoding = new_cte


def _generate_form_data(**kwargs: Union[Any, BotoFairu]) -> aiohttp.FormData:
    form_fata = aiohttp.FormData()

    for name, value in kwargs.items():
        if isinstance(value, BotoFairu):
            form_fata.add_field(
                name, value._content,
                content_type=value._content_type,
                filename=value._filename,
                content_transfer_encoding=value._content_transfer_encoding)

        elif isinstance(value, (list, dict)):
            form_fata.add_field(name, json.dumps(value))

        elif isinstance(value, (int, float, str, bool)):
            form_fata.add_field(name, str(value))

        else:
            raise TypeError("Unknown Type: {}".format(type(value)))

    return form_fata


def generate(**kwargs: Any) -> Tuple[
        Dict[str, str], Union[AnyStr, aiohttp.FormData]]:
    headers = {}  # type: Dict[str, str]
    try:
        data = json.dumps(kwargs)
        headers["Content-Type"] = "application/json"

    except:  # Fallback to Form Data.
        data = _generate_form_data(**kwargs)

    return headers, data
