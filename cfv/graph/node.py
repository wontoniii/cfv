class Node:
  def __init__(self):
    '''

    '''
    self.id = 0
    self.fname = ""
    self.params = {}

  def set_fname(self, name):
    '''

    :param name:
    :return:
    '''
    self.fname = name

  def get_fname(self):
    '''

    :return:
    '''
    return self.fname

  def set_parameter(self, key, value):
    '''

    :param key:
    :param value:
    :return:
    '''
    self.params[key] = value

  def get_parameter(self, key):
    '''

    :param key:
    :return:
    '''
    if key in self.params:
      return self.params[key]
    else:
      return None