import asyncio
from cfv.net.port import InPort, OutPort
from cfv.net.message import Message


class RemoteInPort(InPort):
  def __init__(self, callback, host, port, marshalling="json"):
    '''

    '''
    InPort.__init__(self, callback)
    self.marshalling = marshalling.lower()
    self.host = host
    self.port = port
    self.reader = None
    self.writer = None

  async def setup(self):
    '''
    Start server listening for incoming connections

    :return:
    '''
    await asyncio.start_server(self.client_connected, self.host, self.port)

  async def client_connected(self, reader, writer):
    '''

    :param reader:
    :param writer:
    :return:
    '''
    # Log the new client
    self.reader = reader
    self.writer = writer

  async def push(self, msg):
    '''
    Pushing message from network

    :param msg:
    :return:
    '''
    if self.writer is None:
      #throw error
      return
    elif msg is None:
      return
    await self.writer()

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



class RemoteOutPort(OutPort):
  def __init__(self, remoteIp, remotePort, marshalling="JSON"):
    '''

    '''
    OutPort.__init__(self, None)
    self.marshalling = marshalling
    self.remoteIp = remoteIp
    self.remotePort = remotePort
    self.reader = None
    self.writer = None

  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    return

  async def push(self, msg):
    '''
    Pushing message over network

    :param msg:
    :return:
    '''
    if self.writer is None:
      #throw error
      return
    elif msg is None:
      return
    await self.writer()