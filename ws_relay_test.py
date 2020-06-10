import discord
import websockets
import asyncio


class RelayClient(discord.Client):
    def __init__(self):
        super(RelayClient, self).__init__()
        self.sock = None
        self.last_message = None

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.dm_user = self.get_user(213783701278949376)

    async def on_message(self, message):
        if message.author == self.user or message.author != self.dm_user:
            return

        await self.sock.send(message.content)

        self.last_message = message


    async def handler(self, websocket, path):
        self.sock = websocket
        async for message in websocket:
            message = " ".join(message.split())
            if message.startswith('$react'):
                await self.last_message.add_reaction(message.split(' ')[1])
            else:
                self.last_message = await self.dm_user.send(message)

    def run(self):
        asyncio.get_event_loop().create_task(websockets.serve(self.handler, "localhost", 6789))
        super().run()


RelayClient().run()
