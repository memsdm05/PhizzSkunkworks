import asyncio
import websockets
import emoji

def isEmoji(chr):
    return len(chr) == 1 and chr in emoji.UNICODE_EMOJI

async def send_and_print(websocket : websockets.WebSocketClientProtocol, message):
    print('< ' + message)
    await websocket.send(message)

async def hello():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print('> ' + message)
            if isEmoji(message):
                await send_and_print(websocket, f'$react {message}')
            elif message == 'p.ping':
                await send_and_print(websocket, 'pong!')
            else:
                await send_and_print(websocket, message[::-1])

asyncio.get_event_loop().run_until_complete(hello())

