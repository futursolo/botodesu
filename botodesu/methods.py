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
Auto expanding API methods.
"""

from typing import Dict

from . import exceptions

import threading
import re

_GLOBAL_LOCK = threading.Lock()

_ALLOWED_NAME = re.compile(r"^[a-z]([a-z\_]+)?$")


class _BotoMethods(Dict[str, str]):
    def __getitem__(self, name: str) -> str:
        if name not in self.keys():
            with _GLOBAL_LOCK:
                if re.fullmatch(_ALLOWED_NAME, name) is None:
                    raise exceptions.BotoEra(
                        ("Unacceptable API Method Name: {}, "
                         "r\"^[a-z]([a-z\_]+)?$\" is expected.").format(name))

                self[name] = name.strip().replace("_", "")

        return dict.__getitem__(self, name)


_BOTO_METHODS = _BotoMethods()


def get_url_name(attr_name: str) -> str:
    return _BOTO_METHODS[attr_name]
