from cfv.functions.function import Function
from cfv.net.message import Message
import logging
import datetime

class VideoSink(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)

  def push(self, msg):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}. Discarding it".format(datetime.datetime.now().timestamp()))

  async def push_async(self, msg):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}. Discarding it".format(datetime.datetime.now().timestamp()))
