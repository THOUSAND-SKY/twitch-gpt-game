import os
import reactivex as rx
from reactivex import operators as ops
from twitchio.ext import commands


class Bot(commands.Bot):
    chat = rx.Subject()

    def __init__(self, token=None):
        if token == None:
            token = os.getenv("TWITCH_TOKEN")
        if token == None:
            print("TWITCH_TOKEN missing!")
            exit(1)
        channel = os.getenv("TWICH_CHANNEL")
        if channel == None:
            print("TWITCH_CHANNEL missing!")
            exit(1)
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=token,
                         prefix="!",
                         initial_channels=[channel])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        if self._on_ready_cb != None:
            self._on_ready_cb()

    def on_ready(self, cb):
        self._on_ready_cb = cb

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        print("Message received")
        # Print the contents of our message to console...
        self.chat.on_next(message.content)
