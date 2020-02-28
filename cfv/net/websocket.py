import aiohttp
from aiohttp import web
import logging

from cfv.net.message import Message
from cfv.utils.performance import Performance

class WebSocketServer:
  CLIENT_MAX_SIZE = 1024*1024*20

  def __init__(self, host, port, callback):
    self.host = host
    self.port = port
    self.application = None
    self.callback = callback

  async def setup(self):
    self.application = web.Application(client_max_size=WebSocketServer.CLIENT_MAX_SIZE)
    self.application.add_routes([web.get('/ws', self.websocket_handler)])

  async def websocket_handler(self, request):
    # READ BODY
    logging.debug("Received new socket connection: {}".format(request.headers))

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for websocket_message in ws:
      if msg.type == aiohttp.WSMsgType.TEXT:
        if websocket_message.data[0] == 'c':
          await ws.close()
        elif websocket_message.data[0] == 'f':
          msg = Message()
          p = Performance()
          p.start()
          msg.unmarshal_json(websocket_message[1:])
          p.end()
          logging.debug("Unmarshalling took {}".format(p.timediff()))
      elif msg.type == aiohttp.WSMsgType.ERROR:
        logging.error('ws connection closed with exception {}'.format(ws.exception()))

    logging.debug('websocket connection closed')

    return ws

  def get_runners(self):
    return [web._run_app(self.application, access_log=None, print=logging.debug)]

  def is_connected(self):
    '''
    Wait until connection is established
    :return:
    '''
    #TODO
    return True


class WebSocketClient:

  def __init__(self, remote_ip, remote_port):
    self.session = None
    self.remote_ip = remote_ip
    self.remote_port = remote_port
    self.url = 'http://{}:{}/ws'.format(remote_ip, remote_port)
    self.ws = None

  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    self.session = aiohttp.ClientSession()
    self.ws = await self.session.ws_connect(self.url)

  async def send(self, msg):
    p = Performance()
    p.start()
    data = msg.marshal_json()
    p.end()
    logging.debug("Marshalling took {}".format(p.timediff()))

    p = Performance()
    p.start()
    resp = await self.ws.send_str(['f'] + data)
    p.end()
    logging.debug("Sending request took {}".format(p.timediff()))
    logging.debug(resp)

