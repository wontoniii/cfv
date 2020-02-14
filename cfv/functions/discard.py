from cfv.functions.function import Function
import logging

class Discard(Function):
  def __init__(self):
    '''

    '''
    Function.__init__(self)
    self.flows = {}

  async def push(self, id, msg):
    '''
    Drops one every two frames
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
