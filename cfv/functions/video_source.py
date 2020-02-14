from cfv.functions.function import Function
from cfv.net.message import Message
import logging
import datetime
import cv2
import asyncio
import random
import string

class VideoSource(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)
    self.video_source = ""


  def configure(self, config):
    if "source" not in config.keys():
      raise ValueError("Missing source parameter")
    self.video_source = config["source"]


  def push(self, msg):
    '''

    :param port:
    :return:
    '''
    logging.warning("Received frame at time {}. This should not happen".format(datetime.datetime.now().timestamp()))


  async def run(self):
    '''

    :return:
    '''
    logging.debug("Starting streaming of source {}".format(self.video_source))
    if not len(self.outgoing):
      logging.error("Not out ports set")
      return

    flow_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    cap = cv2.VideoCapture(self.video_source)

    async def read_frame():
      logging.debug("Reading next frame from {}".format(self.video_source))
      ret, img = cap.read()
      if (type(img) == type(None)):
        logging.warning("No frame left to read from {}.".format(self.video_source))
        return None

      logging.debug("Read frame. ret={}.".format(ret))
      msg = Message()
      msg.set_frame(img)
      msg.set_argument("flow_id", flow_id)
      return msg

    while True:
      task = asyncio.create_task(read_frame())
      msg = await task
      if msg is None:
        return
      await self.outgoing[0].push(msg)


  def get_async_tasks(self):
    '''

    :return:
    '''
    return Function.get_async_tasks(self) + [self.run()]
