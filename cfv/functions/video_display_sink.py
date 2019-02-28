from cfv.functions.function import Function
from cfv.net.message import Message
import logging
import datetime
import cv2

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
    logging.debug("Received frame at time {}. Displaying it".format(datetime.datetime.now().timestamp()))
    cv2.imshow('video', msg.get_frame())

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
