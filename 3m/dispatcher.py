import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
import tornado.web as http
import logging
import sys

logging.basicConfig(format='[%(asctime)-15s] %(message)s', level=logging.INFO)

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

def main():
    redirect_url = {"url": "https://example.com"}

    # create a tornado application and provide the urls
    app = tornado.web.Application([(r'/', Dispatcher),
                                   (r'/health', HealthCheck),
                                   (r'/redirect', http.RedirectHandler, redirect_url)])

    # setup the server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(int(sys.argv[1]))
    # start io/event loop
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()