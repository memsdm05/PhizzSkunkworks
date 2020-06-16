import asyncio
import logging
import sys
import platform
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

logging.basicConfig(format='[%(asctime)-15s][AUTO+A] %(message)s', level=logging.INFO, stream=sys.stdout)

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

    logging.info(f'Hosting Autobahn + Asyncio server on {IP}:{str(PORT)}')

    factory = WebSocketServerFactory()
    factory.protocol = EchoWSHandler

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, IP, PORT)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()