import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpserver

import sys
import logging
import platform
import asyncio

logging.basicConfig(format='[%(asctime)-15s][TORN] %(message)s', level=logging.INFO, stream=sys.stdout)

IP = "localhost"
PORT = 4000

class EchoWSHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        logging.info(f'[{len(self.clients)}] New Client')

    def on_message(self, message):
        self.write_message(message)
        logging.info(f'[{len(self.clients)}] Echoed: {message}')

    def on_close(self):
        self.clients.remove(self)
        logging.info(f'[{len(self.clients)}] Client Left')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.info(f'Hosting Tornado server on {IP}:{str(PORT)}')

    # create app
    app = tornado.web.Application([(r'/', EchoWSHandler)])

    # setup the server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(PORT, IP)

    # start io/event loop
    tornado.ioloop.IOLoop.current().start()

