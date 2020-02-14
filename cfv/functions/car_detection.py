from cfv.functions.function import Function
import logging
import datetime
import cv2

class CarDetection(Function):
  def __init__(self, cascade_src):
    '''

    '''
    Function.__init__(self)
    self.car_cascade = cv2.CascadeClassifier(cascade_src)

  async def push(self, id, msg):
    '''

    :param port:
    :return:
    '''
    logging.debug("Received frame at time {} from port {}".format(datetime.datetime.now().timestamp(), id))
    cars = self.car_cascade.detectMultiScale(msg.get_frame(), 1.1, 1)

    logging.debug("Applied car detection at time {}".format(datetime.datetime.now().timestamp()))

    for (x, y, w, h) in cars:
      cv2.rectangle(msg.get_frame(), (x, y), (x + w, y + h), (0, 0, 255), 2)

    await self.outgoing[0].push(msg)
