from cfv.functions.function import Function
from cfv.net.message import Message
import logging
import datetime

class Discard(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)
    self.flows = {}

  def push(self, msg):
    '''

    :param port:
    :return:
    '''
    flow_id = msg.get_argument("flow_id")
    if flow_id is None:
      logging.debug("Flow does not have id, won't discard")
    else:
      if flow_id not in self.flows.keys():
        logging.debug("New flow {} received".format(flow_id))
        self.flows[flow_id] = -1
      self.flows[flow_id] += 1
      if self.flows[flow_id] % 2 == 1:
        logging.debug("Even frame {}, discarding".format(self.flows[flow_id]))
        return
      else:
        self.outgoing[0].push(msg)


  async def push_async(self, msg):
    '''

    :param port:
    :return:
    '''
    flow_id = msg.get_argument("flow_id")
    if flow_id is None:
      logging.debug("Flow does not have id, won't discard")
    else:
      if flow_id not in self.flows.keys():
        logging.debug("New flow {} received".format(flow_id))
        self.flows[flow_id] = -1
      self.flows[flow_id] += 1
      if self.flows[flow_id] % 2 == 1:
        logging.debug("Even frame {}, discarding".format(self.flows[flow_id]))
        return
      else:
        await self.outgoing[0].push(msg)
