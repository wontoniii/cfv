import logging
import datetime
import asyncio

class Function:
  def __init__(self):
    '''

    '''
    self.outgoing = []
    self.incoming = []


  def configure(self, config):
    '''

    :param config:
    :return:
    '''
    pass


  def add_outgoing_port(self, port):
    '''

    :param port:
    :return:
    '''
    self.outgoing.append(port)


  def add_incoming_port(self, port):
    '''

    :param port:
    :return:
    '''
    self.incoming.append(port)


  async def push(self, id, frame):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}".format(datetime.datetime.now().timestamp()))


  async def run(self):
    '''

    :return:
    '''
    logging.warning("Nothing to run for this function")


  def get_async_tasks(self):
    '''

    :return:
    '''
    tasks = []
    for port in self.incoming + self.outgoing:
      tasks += port.get_runners()
    return tasks

