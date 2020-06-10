'''
    This module hosts a websocket server using tornado
    libraries
'''

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
from tornado.options import define, options
import time
import sys
import ipy_autoreload

class WebSocketHandler(ws.WebSocketHandler):
    '''
    This class handles the websocket channel
    '''

    clients = []

    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def open(self):
        '''
            client opens a connection
        '''
        self.clients.append(self)
        print("New client connected")

    def on_message(self, message):
        '''
            Message received on the handler
        '''
        print(f"[{len(self.clients)}] received message {message.strip()}")
        self.write_message(message[::-1])

    def on_close(self):
        '''
            Channel is closed
        '''
        self.clients.remove(self)
        print("connection is closed")

    def check_origin(self, origin):
        return True


def initiate_server():
    # create a tornado application and provide the urls
    app = tornado.web.Application(WebSocketHandler.route_urls())

    # setup the server
    server = tornado.httpserver.HTTPServer(app)
    server.listen(int(sys.argv[1]))
    # start io/event loop
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    initiate_server()
