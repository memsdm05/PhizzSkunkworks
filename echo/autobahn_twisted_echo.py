'''
Cannot run on windows, also bad
'''

import sys
from twisted.internet import reactor


import asyncio
import logging
import platform
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

logging.basicConfig(format='[%(asctime)-15s][AUTO+T] %(message)s', level=logging.INFO, stream=sys.stdout)

IP = "localhost"
PORT = 4000

class EchoWSHandler(WebSocketServerProtocol):
    clients = set()

    def onConnect(self, request):
        logging.info(f'[{len(self.clients)}] New Connection')

    def onOpen(self):
        self.clients.add(self)
        logging.info(f'[{len(self.clients)}] New Client')

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)
        logging.info(f'[{len(self.clients)}] Echoed: {payload.decode("utf8")}')

    def onClose(self, wasClean, code, reason):
        self.clients.remove(self)
        logging.info(f'[{len(self.clients)}] Client Left')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.info(f'Hosting Autobahn + Twisted server on {IP}:{str(PORT)}')

    factory = WebSocketServerFactory()
    factory.protocol = EchoWSHandler
    factory.setProtocolOptions(maxConnections=9999999)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(PORT, factory)
    reactor.run()
