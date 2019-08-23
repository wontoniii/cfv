import asyncio

class InPort():
  def __init__(self, callback):
    '''
    General definition of incoming port
    '''
    self.callback = callback

  def get_runners(self):
    return []


class OutPort():
  def __init__(self, nextPort):
    '''
    General definition of outgoing port
    '''
    self.nextPort = nextPort

  def get_runners(self):
    return []

