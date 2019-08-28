import datetime

class Performance:

  def __init__(self):
    self._start_ts = None
    self._end_ts = None

  def start(self):
    self._start_ts = datetime.datetime.now()

  def end(self):
    self._end_ts = datetime.datetime.now()

  def timediff(self):
    diff = self._end_ts - self._start_ts
    return diff.total_seconds() * 1000