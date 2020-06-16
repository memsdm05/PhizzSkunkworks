'''
WIP
'''

import websockets
import asyncio
import sys

class ClientHandler:
    clientnum = 0

    @classmethod
    async def handler(self, uri):
        async with websockets.connect(uri) as ws:
            await ws.send('client' + self.clientnum)
            self.clientnum += 1

