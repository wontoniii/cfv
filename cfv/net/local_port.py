import asyncio
from cfv.net.port import InPort, OutPort


class LocalInPort(InPort):
  '''
  Incoming port that uses local queues to handle message passing.
  '''
  def __init__(self, id, callback, asynchronous=True):
    '''
    Instantiate a new port and set the callback call
    :param id: Port identifier
    :param callback: Function to call when a new message is received
    :param asynchronous: Whether to run the port in asynchronous mode
    '''
    InPort.__init__(self, id, callback)
    self.asynchronous = asynchronous
    if self.asynchronous:
      self.queue = asyncio.Queue()
    else:
      self.queue = None
    self.canceled = False

  async def push(self, msg):
    '''
    Pass a message into the port
    :param msg: Message to pass
    :return:
    '''
    if self.asynchronous:
      self.queue.put_nowait(msg)
    else:
      await self.callback(self.id, msg)

  async def run(self):
    '''
    Control loop to continously read messages in queue
    :return:
    '''
    while not self.canceled:
      task = asyncio.create_task(self.queue.get())
      msg = await task
      await self.callback(self.id, msg)

  def get_runners(self):
    '''
    Get the tasks to run in asynchronous mode
    :return: self.run if is asynchronous
    '''
    if self.asynchronous:
      return [self.run()]
    else:
      return []


class LocalOutPort(OutPort):
  def __init__(self, id, nextPort, asynchronous=True):
    '''

    :param id: Port identifier
    :param nextPort: InPort to send messages to
    :param asynchronous: Whether to run the port in asynchronous mode
    '''
    OutPort.__init__(self, id, nextPort)
    self.asynchronous = asynchronous


  async def push(self, msg):
    '''
    Pass a message to the next port
    :param msg: Message to pass
    :return:
    '''
    await self.nextPort.push(msg)