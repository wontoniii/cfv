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

  def run(self):
    '''

    :return:
    '''
    pass

  async def run_async(self):
    '''

    :return:
    '''
    #I guess it should start all incoming ports?
    pass
