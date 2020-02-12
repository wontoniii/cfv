import json

from cfv.graph.node import Node

class Graph:

  def __init__(self):
    '''

    '''
    self.nodes = []
    self.map_to_nodes = {}


  def load_from_json(self, filename):
    '''

    :param filename:
    :return:
    '''
    with open(filename, "r") as f:
      json_data = json.loads(f)

      if "nodes" not in json_data.keys():
        raise ValueError("No nodes configuration in the file")

      nodes = json_data["nodes"]
      for i, node in enumerate(nodes):
        new_node = Node()
        new_node.id = i
        name = str(i)
        if "name" in node.keys():
          name = node["name"]
        if name in self.map_to_nodes.keys():
          raise ValueError("Node with name {} already exists".format(name))
        new_node.set_name(name)
        if "type" not in node.keys():
          raise ValueError("Function type is required for all nodes")
        new_node.set_type(node["type"])


  def get_node_by_id(self, id):
    '''

    :param id:
    :return:
    '''
    if len(self.nodes) < id:
      raise ValueError("No node with id {}".format(id))
    return self.nodes[id]


  def get_node_by_name(self, name):
    '''

    :param id:
    :return:
    '''
    if name.lower() not in self.map_to_nodes.keys():
      raise ValueError("No node with that id")
    return self.nodes[self.map_to_nodes[name.lower()]]