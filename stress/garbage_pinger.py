'''
'''

import websockets
import asyncio
import random as r
import string
from datetime import datetime
import sys
import time
import logging

logging.basicConfig(format="")

count = 0
chars = 0

def timeprint(txt: str):
    print(f'[{datetime.now().isoformat()}] {txt}')

async def getGarbage(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((r.choice(lettersAndDigits) for i in range(stringLength)))

async def handler(uri):
    global count, chars
    async with websockets.connect(uri) as websocket:
        while True:
            garbage = await getGarbage(r.randint(8, 30))

            start = time.time()
            await websocket.send(garbage)
            back = await websocket.recv()
            end = time.time()
            timeprint(f'SENT {garbage:>30}  RECEIVED {back:>30}  PING {round((end - start)*1000):>5}')

            chars += len(garbage)
            count += 1

            await asyncio.sleep(r.random()*3)

uri = sys.argv[1]
loop = asyncio.get_event_loop()

try:
    for i in range(int(sys.argv[2])):
        loop.create_task(handler(uri))
    loop.run_forever()
except KeyboardInterrupt:
    timeprint(f'SENT {chars} CHARACTERS {count} TIMES TO {uri}')
except websockets.exceptions.ConnectionClosedError:
    timeprint('CONNECTION CLOSED ABNORMALLY')