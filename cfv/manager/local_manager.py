import asyncio
import logging
from cfv.manager.graph import Graph
from cfv.net.local_port import *
from cfv.net.remote_port import *

from cfv.functions.functions_directory import get_class_by_name

class LocalManager:
  '''

  '''

  def __init__(self):
    '''

    '''
    self.graph = None
    self.functions = {}
    self.tasks = []


  def process_config_json(self, filename):
    '''

    :param filename: the pat to the json file to process
    :return:
    '''
    logging.debug("Loading configuration file {}".format(filename))
    g = Graph()
    g.load_from_json(filename)
    self.graph = g


  async def start_functions(self):
    '''

    :return:
    '''
    for node in self.graph.iter_nodes():
      #initialize function
      logging.debug("Working on node {}".format(node))
      class_ = get_class_by_name(node.type)
      logging.debug("Creating node {} of type {}".format(node.name, node.type))
      f = class_()
      f.configure(node.parameters)
      #add and start ports
      for i in node.in_ports:
        port = node.in_ports[i]
        if True:  # TODO for the time being, everything is async
          if port.local:
            p = LocalInPortAsync(f.push_async)
          else:
            p = RemoteInPort(f.push_async, port.local_ip, port.local_port)
          f.add_incoming_port(p)
        else:
          raise Exception("No support for synchronous ports yet")

      self.functions[node.name] = f

    for node in self.graph.iter_nodes():
      f = self.functions[node.name]
      for i in node.out_ports:
        port = node.out_ports[i]
        other_edge = self.graph.get_node_by_name(port.remote_vertex_name).in_ports[port.remote_edge_id]
        other_port = self.functions[port.remote_vertex_name].incoming[port.remote_edge_id]
        if True:  # TODO for the time being, everything is async
          if port.local:
            p = LocalOutPortAsync(other_port)
          else:
            p = RemoteOutPort(other_edge.local_ip, other_edge.local_port)
          f.add_outgoing_port(p)
        else:
          raise Exception("No support for synchronous ports yet")

    for f in self.functions.values():
      to_add = f.get_async_tasks()
      if len(to_add) > 0:
        self.tasks.extend(to_add)

    logging.debug("About to run tasks {}".format(self.tasks))

    await asyncio.gather(*self.tasks)