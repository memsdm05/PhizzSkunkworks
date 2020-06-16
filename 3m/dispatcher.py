import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
import tornado.web as http
import logging
import asyncio
import platform
import sys

logging.basicConfig(format='[%(asctime)-15s] %(message)s', level=logging.INFO, stream=sys.stdout)

clients = {}

class HealthCheck(http.RequestHandler):
    def get(self):
        self.write(f'<b>There are {len(clients)} users</b><br>{", ".join(clients.keys()).rstrip(", ")}')

class Dispatcher(ws.WebSocketHandler):
    def initialize(self):
        self.name = ''
        self.hasConnected = False

    def on_message(self, message):
        message = message.strip()
        if not self.hasConnected:
            clients[message] = self
            self.name = message
            self.hasConnected = True
            logging.info(f'user {message} connected')
        else:
            routeto = message.split(' ')[0]
            send = ' '.join(message.split(' ')[1:])
            try:
                clients[routeto].write_message(send)
                logging.info(f'{self.name} sent \"{send}\" to {routeto}')
            except:
                clients[self.name].write_message('ERROR could not send')
                logging.error(f'could not send \"{send}\" to {routeto}')

    def on_close(self):
        del clients[self.name]
        logging.info(f'user {self.name} disconnected')

# IP   = '192.168.1.149'
IP   = 'localhost'
PORT = 4000

def main():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    redirect_url = {"url": "https://example.com"}
    handlers = [(r'/', Dispatcher), (r'/health', HealthCheck), (r'/redirect', http.RedirectHandler, redirect_url)]
    # handlers = [(r'/', Dispatcher)]

    # create a tornado application and provide the urls

    app = tornado.web.Application(handlers)

    # setup the server
    server = tornado.httpserver.HTTPServer(app)

    print(f'Hosting server on {IP}:{str(PORT)}')
    server.listen(PORT, IP)
    # start io/event loop
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()