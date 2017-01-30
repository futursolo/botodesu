ボットです(Bo-to Desu!)！
=======================
An automatically expanding Telegram bot API that supports the latest Telegram features.

Documentation
-------------
The documentation of Botodesu is on `Read the docs <https://botodesu.readthedocs.io>`_.

Example
-------
An Echo Bot:

.. code-block:: python

  async with botodesu.Boto("YOUR_API_KEY") as boto:
      async for update in boto:
          if "message" not in update.keys():
              continue

          message = update.message

          if "text" not in message.keys():
              continue

          text = message.text

          await boto.send_message(
              chat_id=message.chat.id,
              text="You said: \"{}\".".format(text),
              reply_to_message_id=message.message_id)

Prerequisites
-------------
- `python_version>=3.5.2`
- `aiohttp>=1.2.0`

Try it out!
-----------
.. code-block:: shell

  $ pip install -U botodesu

License
-------
MIT License

Copyright (c) 2017 Kaede Hoshikawa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
