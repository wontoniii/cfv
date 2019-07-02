import asyncio
from cfv.net.port import InPort, OutPort


class LocalInPort(InPort):
  '''
  Incoming port that uses local queues to handle message passing.
  '''
  def __init__(self, callback):
    '''
    Instantiate a new porrt and set the callback call
    :param callback: Function to call when a new message is received
    '''
    InPort.__init__(self, callback)

  def push(self, msg):
    '''
    Pass a message into the port
    :param msg: Message to pass
    :return:
    '''
    self.callback(msg)


class LocalInPortAsync(InPort):
  def __init__(self, callback):
    '''

    '''
    InPort.__init__(self, callback)
    self.queue = asyncio.Queue()
    self.canceled = False

  async def push(self, msg):
    self.queue.put_nowait(msg)

  async def run(self):
    while not self.canceled:
      task = asyncio.create_task(self.queue.get())
      msg = await task
      await self.callback(msg)




class LocalOutPort(OutPort):
  def __init__(self, nextPort):
    '''

    '''
    OutPort.__init__(self, nextPort)

  def push(self, msg):
    self.nextPort.push(msg)


class LocalOutPortAsync(OutPort):
  def __init__(self, nextPort):
    '''

    '''
    OutPort.__init__(self, nextPort)

  async def push(self, msg):
    # print("I'm the out port {}  --{}".format(self.nextPort, self.nextPort.push))
    await self.nextPort.push(msg)