import asyncio
import logging
import sys
import platform
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

logging.basicConfig(format='[%(asctime)-15s][PROTO] %(message)s', level=logging.INFO, stream=sys.stdout)

IP = "localhost"
PORT = 4000

class Dispatch(WebSocketServerProtocol):
    clients = {}
    isThereBot = False

    def onConnect(self, request):
        self.isBot = False
        self.clientName = ''
        logging.info(f'[{len(self.clients)}] New Connection')

    def onOpen(self):
        self.registerClient()

    def onMessage(self, payload, isBinary):
        message = payload.decode('utf8')
        if message == 'bot':
            self.upgradeToBot()
        else:
            if self.isBot:
                self.botToClient(message, isBinary)
            else:
                self.clientToBot(message, isBinary)


    def onClose(self, wasClean, code, reason):
        if self.isBot:
            del self.clients['bot']
            Dispatch.isThereBot = False
            logging.info(f'[{len(self.clients)}] Bot Left')
        else:
            del self.clients[self.clientName]
            logging.info(f'[{len(self.clients)}] Client {self.clientName} Left')

    def registerClient(self):
        # Client Register
        self.clientName = 'c' + str(len(self.clients))
        self.clients[self.clientName] = self

        logging.info(f'[{len(self.clients)}] New Client ({self.clientName}) Created')

    def upgradeToBot(self):
        # Bot Register
        old = self.clientName
        del self.clients[old]
        self.clientName = 'bot'
        self.clients[self.clientName] = self

        self.isBot = True
        Dispatch.isThereBot = True

        logging.info(f'[{len(self.clients)}] {old} upgraded to bot')

    def botToClient(self, message, isBinary):
        # Bot to Client
        r = message.split(' ')[0]
        p = message.split(' ')[1]
        self.clients[r].sendMessage(p.encode('utf8'), isBinary)
        logging.info(f'[{len(self.clients)}] Sent "{message}" to {r}')

    def clientToBot(self, message, isBinary):
        # Client to Bot
        if Dispatch.isThereBot:
            self.clients['bot'].sendMessage((self.clientName + ' ' + message).encode('utf8'), isBinary)
            logging.info(f'[{len(self.clients)}] {self.clientName} sent "{message}" to bot')
        else:
            logging.error(f'[{len(self.clients)}] {self.clientName} tried '
                          f'to send "{message}" but there is no bot')



if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.info(f'Hosting Autobahn + Asyncio server on {IP}:{str(PORT)}')

    factory = WebSocketServerFactory()
    factory.protocol = Dispatch

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