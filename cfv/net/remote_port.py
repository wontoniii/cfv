import asyncio
import logging
from cfv.net.port import InPort, OutPort
from cfv.net.message import Message
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
    self.application = web.Application(client_max_size=1024*1024*10)
    self.application.add_routes([web.post('/', self.post)])


  async def post(self, request):
    #READ BODY
    logging.debug("Received new http post")
    json_body = await request.text()
    msg = Message()
    msg.unmarshal_json(json_body)
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
    self.session = aiohttp.ClientSession()


  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    #send an empty message to setup the connection


  async def push(self, msg):
    '''
    Pushing message over network

    :param msg:
    :return:
    '''
    print(type(msg.get_frame()), msg.get_frame().dtype)
    logging.debug("Sending http post")
    resp = await self.session.post('http://localhost:8080', data=msg.marshal_json(), headers={'content-type': 'application/json', 'CONNECTION': 'keep-alive'})
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
