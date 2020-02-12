class Edge:
  '''

  '''

  def __init__(self):
    '''

    '''
    self.id = 0
    self.remote_id = 0
    self.local = True
    self.local_ip = "0.0.0.0"
    self.local_port = 8080
    self.remote_vertex_name = ""
    self.remote_edge_id = 0

  def configure(self, config):
    '''

    :param config:
    :return:
    '''
    if "id" in config.keys():
      self.id = config["id"]
    if "remote_id" in config.keys():
      self.remote_id = config["remote_id"]
    if "local_ip" in config.keys():
      self.local_ip = config["local_ip"]
    if "local_port" in config.keys():
      self.local_port = config["local_port"]
    if "remote_vertex_name" in config.keys():
      self.remote_vertex_name = config["remote_vertex_name"]
    if "remote_edge_id" in config.keys():
      self.remote_edge_id = config["remote_edge_id"]