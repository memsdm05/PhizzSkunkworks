import asyncio
import argparse
import time
import platform
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

def getArgs(args=None):
    parser = argparse.ArgumentParser(description='A websocket mass pinger for testing purposes')

    parser.add_argument('--port', '-P', dest='port', type=int, default=4000,
                        help='The port to connect to (default: 4000)')
    parser.add_argument('--uri', '-U', dest='uri', type=str, default='localhost',
                        help='The uri or ip to connect to (default: localhost)')
    parser.add_argument('--secure', '-s', dest='isSecure', action='store_true', default=False,
                        help='Uses WSS instead of WS')
    parser.add_argument('--connections', '-c', dest='conns', type=int, default=1,
                        help='How many connections to the ws server (default: 1)')
    parser.add_argument('--threads', '-t', dest='threads', type=int, default=0,
                        help='How many threads to run the connections in, 0 for no threads (default: 0')

    parser.add_argument('--highest-delay', '-D', dest='high', type=int, default=3)
    parser.add_argument('--lowest-delay', '-d', dest='low', type=int, default=0)
    parser.add_argument('--integer-random', '-r', dest='int_rand', action='store_true', default=False,
                        help='will use random.randint instead of uniform to set delay times')
    parser.add_argument('--no-random-delay', '-N', dest='no_random_delay', action='store_true', default=False,
                        help='Sets the delay to only delay at lowest delay')

    parser.add_argument('--highest-length', '-L', dest='high', type=int, default=10)
    parser.add_argument('--lowest-length', '-l', dest='low', type=int, default=30)
    parser.add_argument('--no-random-length', '-n', dest='no_random_length', action='store_true', default=False,
                        help='Sets the message length to lowest length set')
    parser.add_argument('--binary', '-b', action='store_true', default=False,
                        help='Sends random bytes instead of random strings')

    parser.add_argument('--do-not-measure-ping', '-p', dest='no_ping', action='store_true', default=False,
                        help='Do not measure ping')
    parser.add_argument('--run-once', '-o', dest='once', action='store_true', default=False,
                        help='Ping once then die like the crap that you are')
    parser.add_argument('--message', '-m', dest='message', type=str, default='',
                        help='Send this message instead of random garbage')
    parser.add_argument('--input', '-i', dest='input', type=str, default='',
                        help='Read a control file and create subprocess (IO is disabled)')
    parser.add_argument('--output' '-o', dest='output', type=str, default='',
                        help='Outputs data to a specified text files')

    if args == None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    args = getArgs()

    factory = WebSocketClientFactory()
    factory.protocol = GarbagePingerProtocol

    uri = 'wss' if args.isSecure else 'ws' + '://' + args.uri

    loop = asyncio.get_event_loop()
    for _ in range(args.conns):
        loop.run_until_complete(loop.create_connection(factory, 'wss://echo.websocket.org', 8080, ssl=True))
    loop.run_forever()
    loop.close()