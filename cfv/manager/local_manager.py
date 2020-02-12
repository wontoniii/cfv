import asyncio
from cfv.manager.graph import Graph
from cfv.net.local_port import LocalInPort, LocalOutPort
from cfv.net.remote_port import RemoteInPort, RemoteOutPort

import cfv.functions as functions

class LocalManager:
  '''

  '''

  def __init__(self):
    '''

    '''
    self.graph = None
    self.functions = []
    self.tasks = []


  def process_config_json(self, filename):
    '''

    :param filename: the pat to the json file to process
    :return:
    '''
    g = Graph()
    g.load_from_json(filename)
    self.graph = g


  async def start_functions(self):
    '''

    :return:
    '''
    for node in self.graph.iter_nodes():
      #initialize function
      class_ = getattr(functions, node.get_name())
      f = class_()
      #add and start ports
      for i in node.in_ports:
        port = node.in_ports[i]
        if True:  # TODO for the time being, everything is async
          if port.local:
            p = LocalInPort(f.push_async)
          else:
            p = RemoteInPort(f.push_async, port.local_ip, port.local_port)
          f.add_incoming_port(p)
        else:
          raise Exception("No support for synchronous ports yet")

      for i in node.out_ports:
        port = node.out_ports[i]
        other_edge = self.graph.get_node_by_name(port.remote_vertex_name).in_ports[port.remote_edge_id]
        if True:  # TODO for the time being, everything is async
          if port.local:
            p = LocalOutPort(other_edge)
          else:
            p = RemoteOutPort(other_edge.local_ip, other_edge.local_port)
          f.add_outgoing_port(p)
        else:
          raise Exception("No support for synchronous ports yet")

      self.functions.append(f)

    for f in self.functions:
      to_add = f.get_async_tasks()
      if len(to_add) > 0:
        self.tasks.extend(to_add)

    await asyncio.gather(*self.tasks)