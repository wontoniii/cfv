import asyncio

class InPort():
  def __init__(self, callback):
    '''

    '''
    self.callback = callback


class OutPort():
  def __init__(self, nextPort):
    '''

    '''
    self.nextPort = nextPort

