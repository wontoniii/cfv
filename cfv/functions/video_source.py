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

  def run(self):
    '''

    :return:
    '''
    if not len(self.outgoing):
      logging.error("Not out ports set")
      return

    flow_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    logging.info("Generating flow {}".format(flow_id))
    cap = cv2.VideoCapture(self.video_source)

    while True:
      ret, img = cap.read()
      if (type(img) == type(None)):
        break

      logging.debug("Read frame. ret={}".format(ret))
      msg = Message()
      msg.set_frame(img)
      msg.set_argument("flow_id", flow_id)

      self.outgoing[0].push(msg)

  async def run_async(self):
    '''

    :return:
    '''
    if not len(self.outgoing):
      logging.error("Not out ports set")
      return

    flow_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    cap = cv2.VideoCapture(self.video_source)

    async def read_frame():
      ret, img = cap.read()
      if (type(img) == type(None)):
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
      # logging.debug("Finished waiting. I am {}".format(self.outgoing))


  def get_async_tasks(self):
    '''

    :return:
    '''
    tasks = []
    if len(self.incoming) > 0:
      tasks = [asyncio.create_task(port.run()) for port in self.incoming]

    tasks.extend([self.run_async()])
    return tasks
