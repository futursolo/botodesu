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

from typing import Any, Optional, Union, Dict, List, AnyStr

__all__ = ["BotoEra", "BotoWarning"]


class BotoEra(Exception):
    """
    Era(Error) occurred inside the Botodesu.
    This gives you the ability to retrieve the response information
    from the server if available.
    """
    def __init__(
        self, *args: Any, status_code: Optional[int]=None,
        content: Optional[Union[Dict[str, Any], List[Any], AnyStr]]=None,
            **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.status_code = status_code
        self.content = content


class BotoWarning(Warning):
    """
    The Warning of Botodesu.
    """
    pass
