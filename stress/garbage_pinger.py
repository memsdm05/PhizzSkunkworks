'''
'''

import websockets
import asyncio
import random as r
import string
import sys
import time
import logging

logging.basicConfig(format='[%(asctime)-15s][GPING] %(message)s', level=logging.INFO, stream=sys.stdout)

average = 0
count = 0
chars = 0

async def addToAverage(size, value):
    global average
    average = (size * average + value) / (size + 1)

async def getGarbage(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((r.choice(lettersAndDigits) for i in range(stringLength)))

async def handler(uri):
    global count, chars
    async with websockets.connect(uri) as websocket:
        while True:
            # Generate payload
            garbage = await getGarbage(r.randint(10, 25))

            # Start delta time measure. Send then receive payload. End delta time
            start = time.time()
            await websocket.send(garbage)
            back = await websocket.recv()
            end = time.time()

            # Calculate ping. Increment count
            ping = round((end - start)*1000)
            chars += len(garbage)
            count += 1

            # Add to average and log
            await addToAverage(count, ping)
            logging.info(f'SENT {garbage:>25}  RECEIVED {back:>25}  PING {ping}')

            # Sleepy boi
            await asyncio.sleep(r.random()*3)

uri = sys.argv[1]
loop = asyncio.get_event_loop()

try:
    for i in range(int(sys.argv[2])):
        loop.create_task(handler(uri))
    loop.run_forever()
except KeyboardInterrupt:
    logging.info(f'SENT {chars} CHARACTERS {count} TIMES TO {uri}')
    logging.info(f'AVERAGE PING: {round(average)}')
except websockets.exceptions.ConnectionClosedError:
    logging.info('CONNECTION CLOSED ABNORMALLY')