.. Botodesu documentation master file, created by
   sphinx-quickstart on Mon Jan 30 17:04:41 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ボットです(Bo-to Desu!)！
=========================
An automatically expanding Telegram bot API that supports the latest Telegram features.

Getting Started
---------------
Wait, what? automatically expanding? How does it work?

Unlike the other libraries, the api methods is not pre-defined in this library,
they are defined on the first invocation of the method.
The arguments during the invocation become the corresponding fields in the
form-data which will be encoded into json or urlencoded or multipart
and be submitted with a POST request to the telegram server. Thus,
all the arguments provided when invoking the api methods should be keyword arguments,
because Botodesu has no knowledge of the telegram api in advanced.

Also, to be comply with the PEP8, Botodesu will automatically remove all the
underscores for the api methods.
Please be advised that the Telegram API methods are **case-insensitive**.

Contribution
------------
Botodesu is an early project. All kinds of contributions is warmly welcomed.

The source code is hosted on `GitHub <https://github.com/futursolo/botodesu>`_.

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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
