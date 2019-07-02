import pickle

class Message:
  def __init__(self):
    '''

    '''
    self.frame = None
    self.arguments = {}

  def reset(self):
    '''

    :return:
    '''
    self.frame = None
    self.arguments = {}

  def set_frame(self, frame):
    '''

    :param frame:
    :return:
    '''
    self.frame = frame

  def get_frame(self):
    '''

    :return:
    '''
    return self.frame

  def set_argument(self, key, value):
    '''

    :param key:
    :param value:
    :return:
    '''
    self.arguments[key] = value

  def set_arguments(self, arguments):
    for key in arguments:
      self.arguments[key] = arguments[key]

  def get_argument(self, key):
    '''

    :param key:
    :return:
    '''
    if key not in self.arguments.keys():
      return None
    else:
      return self.arguments[key]

  def get_arguments(self):
    '''

    :return:
    '''
    return self.arguments

  def marshal_json(self):
    '''

    :return:
    '''
    # Creates a sequence of bytes representing the message
    bytes = None
    return bytes

  def unmarshal_json(self, bytes):
    '''

    :return:
    '''
    # Constructs a message from a sequence of bytes
    pass

  def marshal_pickle(self):
    '''

    :return:
    '''
    # Creates a sequence of bytes representing the message
    pkl = pickle.dumps({"frame": self.frame, "args": self.arguments})
    return pkl

  def unmarshal_pickle(self, pkl):
    '''

    :return:
    '''
    # Constructs a message from a sequence of bytes
    msg = pickle.loads(pkl)
    self.frame = msg["frame"]
    self.arguments = msg["args"]