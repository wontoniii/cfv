import cfv.functions as functions
import inspect

class Node:
  def __init__(self):
    '''

    '''
    self.id = 0
    self.name = ""
    self.type = ""
    self.parameters = {}


  def set_name(self, name):
    '''

    :param name:
    :return:
    '''
    self.name = name


  def get_name(self):
    '''

    :return:
    '''
    return self.name


  def set_type(self, t):
    '''

    '''
    if t not in inspect.getmembers(functions):
      raise ValueError("Function type {} is not a valid function type".format(t))
    else:
      self.type = t


  def set_parameter(self, key, value):
    '''

    :param key:
    :param value:
    :return:
    '''
    self.parameters[key] = value

  def get_parameter(self, key):
    '''

    :param key:
    :return:
    '''
    if key in self.parameters:
      return self.parameters[key]
    else:
      return None