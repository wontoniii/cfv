import logging
import datetime

class Function:
  def __init__(self):
    '''

    '''
    self.outgoing = []
    self.incoming = []

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
