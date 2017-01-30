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

try:
    from setuptools import find_packages, setup

except ImportError as e:
    raise RuntimeError("setuptools is required for the installation.")

import sys
import importlib
import os

if not sys.version_info[:3] >= (3, 5, 2):
    raise RuntimeError("Botodesu requires Python 3.5.2 or higher.")


def load_version() -> str:
    _version_spec = importlib.util.spec_from_file_location(
        "botodesu._version",
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "botodesu/_version.py"))
    _version = importlib.util.module_from_spec(_version_spec)
    _version_spec.loader.exec_module(_version)

    return _version.version


setup_requires = ["setuptools"]

install_requires = ["aiohttp>=1.2.0"]
install_requires.extend(setup_requires)

all_requires = ["cchardet>=1.1.2", "aiodns>=1.1.1"]
all_requires.extend(install_requires)

if __name__ == "__main__":
    setup(
        name="botodesu",
        version=load_version(),
        author="Kaede Hoshikawa",
        author_email="futursolo@icloud.com",
        url="https://github.com/futursolo/botodesu",
        license="MIT",
        description=("An automatically expanding Telegram bot API that "
                     "supports the latest Telegram features."),
        long_description=open("README.rst", "r").read(),
        packages=find_packages(),
        include_package_data=True,
        setup_requires=setup_requires,
        install_requires=install_requires,
        zip_safe=False,
        extras_require={
            "all": all_requires
        },
        classifiers=[
            "Operating System :: MacOS",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: CPython"
        ]
    )
