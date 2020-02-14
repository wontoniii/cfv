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
        if port.asynchronous:  # TODO for the time being, everything is async
          if port.local:
            p = LocalInPort(port.id, f.push, asynchronous=True)
          else:
            p = RemoteInPort(port.id, f.push, port.local_ip, port.local_port)
          f.add_incoming_port(p)
        else:
          if port.local:
            p = LocalInPort(port.id, f.push, asynchronous=False)
          else:
            raise Exception("Remote ports can not be synchronous")
          f.add_incoming_port(p)


      self.functions[node.name] = f

    for node in self.graph.iter_nodes():
      f = self.functions[node.name]
      for i in node.out_ports:
        port = node.out_ports[i]
        other_edge = self.graph.get_node_by_name(port.remote_vertex_name).in_ports[port.remote_edge_id]
        other_port = self.functions[port.remote_vertex_name].incoming[port.remote_edge_id]
        if port.asynchronous:  # TODO for the time being, everything is async
          if port.local:
            p = LocalOutPort(port.id, other_port, asynchronous=True)
          else:
            p = RemoteOutPort(port.id, other_edge.local_ip, other_edge.local_port)
          f.add_outgoing_port(p)
        else:
          if port.local:
            p = LocalOutPort(port.id, other_port, asynchronous=False)
          else:
            raise Exception("Remote ports can not be synchronous")
          f.add_outgoing_port(p)

    for f in self.functions.values():
      to_add = f.get_async_tasks()
      if len(to_add) > 0:
        self.tasks.extend(to_add)

    if len(self.tasks) > 0:
      logging.debug("About to run tasks {}".format(self.tasks))
      await asyncio.gather(*[asyncio.create_task(task) for task in self.tasks])