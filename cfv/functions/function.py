class Function:
  def __init__(self):
    '''

    '''
    self.outgoing = []
    self.incoming = []

  def add_outgoing_port(self, port):
    '''

    :param port:
    :return:
    '''
    self.outgoing.append(port)

  def push(self, frame):
    '''

    :param port:
    :return:
    '''
    print "Received frame"
    return
