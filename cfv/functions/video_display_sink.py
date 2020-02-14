from cfv.functions.function import Function
import logging
import datetime
import cv2

class VideoDisplaySink(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)

  async def push(self, id, msg):
    '''
    Displays all incoming frames and then drops them
    :param port:
    :return:
    '''
    logging.debug("Received frame at time {}. Displaying it".format(datetime.datetime.now().timestamp()))
    cv2.imshow('video', msg.get_frame())
    cv2.waitKey(33)
