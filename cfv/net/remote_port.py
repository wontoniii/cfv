import asyncio
import logging

from cfv.net.port import InPort, OutPort
from cfv.net.message import Message
from cfv.net.http import HTTPServer, HTTPClient
from cfv.utils.performance import Performance


class RemoteInPort(InPort):

  def __init__(self, callback, host, port, marshalling="pickle", protocol="http"):
    '''

    '''
    InPort.__init__(self, callback)
    self.canceled = False
    self.connected = False
    self.marshalling = marshalling.lower()
    self.protocol = protocol.lower()
    self.host = host
    self.port = port
    self.queue = asyncio.Queue()
    self.server = None


  async def setup(self):
    '''
    Start server listening for incoming connections

    :return:
    '''
    if self.protocol == "http":
      self.server = HTTPServer(self.host, self.port, self.received)
    else:
      raise TypeError("{} is an invalid connection protocol".format(self.protocol))

    await self.server.setup()


  def is_connected(self):
    '''
    Wait until connection is established
    :return:
    '''
    return self.server.is_connected()


  def get_runners(self):
    runners = [self.run()]
    runners.extend(self.server.get_runners())

    return runners


  async def received(self, msg):
    await self.queue.put(msg)

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
  def __init__(self, remote_ip, remote_port, marshalling="pickle", protocol="http"):
    '''

    '''
    OutPort.__init__(self, None)
    self.canceled = False
    self.marshalling = marshalling
    self.remote_ip = remote_ip
    self.remote_port = remote_port
    self.protocol = protocol
    self.queue = None


  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    self.queue = asyncio.Queue()
    if self.protocol == "http":
      self.server = HTTPClient(self.remote_ip, self.remote_port)
    else:
      raise TypeError("{} is an invalid connection protocol".format(self.protocol))

    await self.server.setup()


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
      await self.server.send(msg)


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
