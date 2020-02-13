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


  def push(self, frame):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}".format(datetime.datetime.now().timestamp()))


  async def push_async(self, frame):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}".format(datetime.datetime.now().timestamp()))


  def run(self):
    '''

    :return:
    '''
    logging.warning("Nothing to run for this function")


  async def run_async(self):
    '''

    :return:
    '''
    logging.warning("Nothing to run for this function")


  def get_async_tasks(self):
    '''

    :return:
    '''
    #I guess it should start all incoming ports?
    if len(self.incoming) > 0:
      return [asyncio.create_task(port.run()) for port in self.incoming]

