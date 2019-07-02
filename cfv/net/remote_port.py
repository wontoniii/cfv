import asyncio
import logging
from cfv.net.port import InPort, OutPort
from cfv.net.message import Message


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
    self.reader = None
    self.writer = None
    self.event_connection = None

  async def setup(self):
    '''
    Start server listening for incoming connections

    :return:
    '''
    self.event_connection = asyncio.Event()
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
    logging.debug("Client connected")
    self.connected = True
    self.event_connection.set()

  def is_connected(self):
    '''
    Wait until connection is established
    :return:
    '''
    if self.connected:
      return True
    else:
      return False

  async def waiter(self, event):
    await event.wait()

  async def run(self):
    if not self.is_connected():
      logging.debug("Client not yet connected")
      awaiter_connection = asyncio.create_task(self.waiter(self.event_connection))
      await awaiter_connection
    while not self.canceled:
      data = await self.reader.read()
      msg = self.unmarshall_message(data)
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
    self.reader = None
    self.writer = None

  async def setup(self):
    '''
    Setup the connection with the remote node

    :return:
    '''
    self.reader, self.writer = await asyncio.open_connection(self.remote_ip, self.remote_port)

  async def push(self, msg):
    '''
    Pushing message over network

    :param msg:
    :return:
    '''
    if self.writer is None:
      #throw error
      logging.error("Working without a writer")
      return
    elif msg is None:
      return
    self.writer.write(self.marshall_message(msg))
    await self.writer.drain()

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
