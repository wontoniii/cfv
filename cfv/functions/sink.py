from cfv.functions.function import Function
import logging
import datetime

class Sink(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)

  async def push(self, id, msg):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}. Discarding it".format(datetime.datetime.now().timestamp()))
