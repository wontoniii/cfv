from cfv.functions.function import Function
from cfv.net.message import Message
import logging
import datetime
import cv2

class VideoSource(Function):
  def __init__(self, video_src):
    '''

    '''
    Function.__init__(self)
    self.video_source = video_src

  def push(self, msg):
    '''

    :param port:
    :return:
    '''
    logging.warning("Received frame at time {}. This should not happen".format(datetime.datetime.now().timestamp()))

  def run(self):
    '''

    :return:
    '''
    if not len(self.outgoing):
      logging.error("Not out ports set")
      return

    cap = cv2.VideoCapture(self.video_source)

    while True:
      ret, img = cap.read()
      if (type(img) == type(None)):
        break

      logging.debug("Read frame. ret={}".format(ret))
      msg = Message()
      msg.set_frame(img)

      self.outgoing[0].push(msg)

  async def run_async(self):
    '''

    :return:
    '''
    self.run()
