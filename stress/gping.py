import asyncio
import argparse
import time
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory
import random as r

class PingStopwatch():
    def __init__(self):
        self.milli = lambda: int(round(time.time() * 1000))
        self.elapsed = 0
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = self.milli()

    def stop(self):
        self._stop = self.milli()
        self.elapsed = self._stop = self._start
        self._stop = 0
        self._start = 0

class GarbagePingerProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        watch = PingStopwatch()


    def onOpen(self):

        def ping():
            self.sendMessage("Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.loop.call_later(r.random()*3, ping)

        # start sending messages every second ..
        ping()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A websocket mass pinger for testing purposes')

    parser.add_argument('--port', '-p', dest='port', type=int, default=4000,
                        help='The port to connect to (default: 4000)')
    parser.add_argument('--ip', '-I', dest='ip', type=str, default='localhost',
                        help='The uri to connect to (default: localhost)')
    parser.add_argument('--wsuri', '-w', dest='uri', type=str, default='',
                        help='The uri of the ws connection. Overwrites PORT and IP')
    parser.add_argument('--connections', '-c', dest='conns', type=int, default=1,
                        help='How many connections to the ws server (default: 1)')
    parser.add_argument('--threads', '-t', dest='threads', type=int, default=0,
                        help='How many threads to run the connections in, 0 for no threads (default: 0')

    parser.add_argument('--highest-delay', '-H', dest='high', type=int, default=3)
    parser.add_argument('--lowest-delay', '-L', dest='low', type=int, default=0)
    parser.add_argument('--integer-random', 'r', action='store_true', default=False)
    parser.add_argument('--no-random-delay', '-n', action='store_true', default=False,
                        help='Sets the delay to only delay at lowest delay')
    parser.add_argument('--binary', '-b', action='store_true', default=False,
                        help='Sends random bytes instead of random strings')
    # TODO Add message length arguments (random, no length)
    parser.add_argument('--do-not-measure-ping', '-p', action='store_true', default=False,
                        help='Do not measure ping')
    parser.add_argument('--run_once', '-o', dest='once', action='store_true', default=False,
                        help='Ping once then die like the crap that you are')
    parser.add_argument('--message', '-m', dest='message', type=str, default='',
                        help='Send this message instead of random garbage')
    parser.add_argument('--input', 'i', dest='input', type=str, default='',
                        help='Read a control file and create subprocess (IO is disabled)')
    parser.add_argument('--output' 'o', dest='output', type=str, default='',
                        help='Outputs data to a specified text files')

    args = parser.parse_args()

    factory = WebSocketClientFactory()
    factory.protocol = GarbagePingerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 4000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()