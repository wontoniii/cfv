import asyncio

class InPort():
  '''
  General definition of incoming port
  '''
  def __init__(self, id, callback):
    '''

    :param id: Port identifier
    :param callback: Callback function to call when receiving a new message
    '''
    self.id = id
    self.callback = callback

  def get_runners(self):
    '''
    Get the tasks to run in asynchronous mode
    :return: []
    '''
    return []


class OutPort():
  '''
  General definition of outgoing port
  '''
  def __init__(self, id, nextPort):
    '''

    :param id: Port identifier
    :param nextPort: InPort to send messages to
    '''
    self.id = id
    self.nextPort = nextPort

  def get_runners(self):
    '''
    Get the tasks to run in asynchronous mode
    :return: []
    '''
    return []

