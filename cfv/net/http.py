import aiohttp
from aiohttp import web
import logging

from cfv.net.message import Message
from cfv.utils.performance import Performance

class HTTPServer:
  CLIENT_MAX_SIZE = 1024*1024*20

  def __init__(self, host, port, callback):
    self.host = host
    self.port = port
    self.application = None
    self.callback = callback

  async def setup(self):
    self.application = web.Application(client_max_size=HTTPServer.CLIENT_MAX_SIZE)
    self.application.add_routes([web.post('/', self.post)])

  async def post(self, request):
    # READ BODY
    logging.debug("Received new http post: {}".format(request.headers))
    p = Performance()
    p.start()
    json_body = await request.text()
    p.end()
    logging.debug("Receiving request took {}".format(p.timediff()))
    msg = Message()
    p = Performance()
    p.start()
    msg.unmarshal_json(json_body)
    p.end()
    logging.debug("Unmarshalling took {}".format(p.timediff()))
    await self.callback(msg)
    return web.Response(status=200)

  def get_runners(self):
    return [web._run_app(self.application)]

  def is_connected(self):
    '''
    Wait until connection is established
    :return:
    '''
    #TODO
    return True


class HTTPClient:

  def __init__(self, remote_ip, remote_port):
    self.session = None
    self.remote_ip = remote_ip
    self.remote_port = remote_port
    self.url = 'http://{}:{}'.format(remote_ip, remote_port)

  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    self.session = aiohttp.ClientSession()

  async def send(self, msg):
    p = Performance()
    p.start()
    data = msg.marshal_json()
    p.end()
    logging.debug("Marshalling took {}".format(p.timediff()))

    p = Performance()
    p.start()
    resp = await self.session.post(self.url, data=data,
                                   headers={'content-type': 'application/json', 'CONNECTION': 'keep-alive'})
    p.end()
    logging.debug("Seding request took {}".format(p.timediff()))
    logging.debug(resp)

