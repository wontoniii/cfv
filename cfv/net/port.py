import asyncio

class InPort():
  def __init__(self, callback):
    '''

    '''
    self.callback = callback


class LocalInPort(InPort):
  def __init__(self, callback):
    '''

    '''
    InPort.__init__(self, callback)

  def push(self, msg):
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
      # await asyncio.sleep(0.1)


class RemoteInPort(InPort):
  def __init__(self, callback, marshalling="JSON"):
    '''

    '''
    InPort.__init__(self, callback)
    self.marshalling = marshalling

  def push(self, msg):
    # Implement pushing over network
    pass


class OutPort():
  def __init__(self, nextPort):
    '''

    '''
    self.nextPort = nextPort


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
    # await asyncio.sleep(0.1)


class RemoteOutPort(OutPort):
  def __init__(self, remoteIp, remotePort, marshalling="JSON"):
    '''

    '''
    OutPort.__init__(self, None)
    self.marshalling = marshalling
    self.remoteIp = remoteIp
    self.remotePort = remotePort
