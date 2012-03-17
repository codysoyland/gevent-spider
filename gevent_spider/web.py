from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import os
from .spider import spider

class Client(object):
    def __init__(self, websocket, env):
        self.ws = websocket
        self.env = env
    def send(self, message):
        self.ws.send(json.dumps(message))
    def receive(self):
        return json.loads(self.ws.receive())
    def send_status(self, message):
        self.send({'cmd': 'status', 'status': message})
    def send_result(self, result):
        self.send({'cmd': 'result', 'result': result})

def application(env, start_response):
    websocket = env.get('wsgi.websocket')

    if not websocket:
        return http_handler(env, start_response)

    client = Client(websocket, env)

    while True:
        message = client.receive()
        cmd = message['cmd']
        if cmd == 'scrape':
            url = message['url']

            spider(client, url).join()
            client.send_status('Done!')

def http_handler(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        yield open(os.path.join(os.path.dirname(__file__), 'media/index.html'), 'r').read()
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        yield '<h1>Not Found</h1>'

def serve():
    WSGIServer(('', 8088), application, handler_class=WebSocketHandler).serve_forever()
