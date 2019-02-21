class Port:
  def __init__(self):
    '''

    '''


class InPort(Port):
  def __init__(self):
    '''

    '''
    Port.__init__(self)


class LocalInPort(InPort):
  def __init__(self):
    '''

    '''
    InPort.__init__(self)


class RemoteInPort(InPort):
  def __init__(self):
    '''

    '''
    InPort.__init__(self)


class OutPort(Port):
  def __init__(self):
    '''

    '''
    Port.__init__(self)

class LocalOutPort(Port):
  def __init__(self):
    '''

    '''
    Port.__init__(self)

class RemoteOutPort(Port):
  def __init__(self):
    '''

    '''
    Port.__init__(self)