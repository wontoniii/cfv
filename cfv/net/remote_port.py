import asyncio
import logging
from cfv.net.port import InPort, OutPort
from cfv.net.message import Message
from cfv.utils.performance import Performance
import aiohttp
from aiohttp import web


class RemoteInPort(InPort):
  def __init__(self, callback, host, port, marshalling="pickle"):
    '''

    '''
    InPort.__init__(self, callback)
    self.canceled = False
    self.connected = False
    self.marshalling = marshalling.lower()
    self.host = host
    self.port = port
    self.application = None
    self.queue = asyncio.Queue()


  async def setup(self):
    '''
    Start server listening for incoming connections

    :return:
    '''
    self.application = web.Application(client_max_size=1024*1024*20)
    self.application.add_routes([web.post('/', self.post)])


  async def post(self, request):
    #READ BODY
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
    await self.queue.put(msg)
    return web.Response(status=200)


  def is_connected(self):
    '''
    Wait until connection is established
    :return:
    '''
    #TODO
    if self.connected:
      return True
    else:
      return False


  def get_runners(self):
    return [web._run_app(self.application), self.run()]


  async def run(self):
    while not self.canceled:
      logging.debug("Create task for queue")
      task = asyncio.create_task(self.queue.get())
      msg = await task
      logging.debug("Read message from queue")
      await self.callback(msg)


  def unmarshall_message(self, data):
    '''

    :param message:
    :return:
    '''
    msg = Message()
    if self.marshalling == 'json':
      msg.unmarshal_json(data)
      return msg
    elif self.marshalling == 'pickle':
      msg.unmarshal_pickle(data)
      return msg
    else:
      msg.unmarshal_json(data)
      return msg



class RemoteOutPort(OutPort):
  def __init__(self, remote_ip, remote_port, marshalling="pickle"):
    '''

    '''
    OutPort.__init__(self, None)
    self.canceled = False
    self.marshalling = marshalling
    self.remote_ip = remote_ip
    self.remote_port = remote_port
    self.queue = None
    self.session = None


  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    self.queue = asyncio.Queue()
    self.session = aiohttp.ClientSession()


  async def push(self, msg):
    '''
    Pushing message over network

    :param msg:
    :return:
    '''
    await self.queue.put(msg)

  def get_runners(self):
    return [self.run()]

  async def run(self):
    while not self.canceled:
      logging.debug("Create task for queue")
      task = asyncio.create_task(self.queue.get())
      msg = await task
      logging.debug("Sending http post")

      p = Performance()
      p.start()
      data = msg.marshal_json()
      p.end()
      logging.debug("Marshalling took {}".format(p.timediff()))

      p = Performance()
      p.start()
      resp = await self.session.post('http://localhost:8080', data=data,
                                     headers={'content-type': 'application/json', 'CONNECTION': 'keep-alive'})
      p.end()
      logging.debug("Seding request took {}".format(p.timediff()))
      logging.debug(resp)


  def marshall_message(self, msg):
    '''

    :param message:
    :return:
    '''
    if self.marshalling == 'json':
      return msg.marshal_json()
    elif self.marshalling == 'pickle':
      return msg.marshal_pickle()
    else:
      return msg.marshal_json()
