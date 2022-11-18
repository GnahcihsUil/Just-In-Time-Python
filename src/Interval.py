class Interval(object):
  def __init__(self, start, end):
    self.start = start
    self.end = end
  
  def __repr__(self):
    return 'Interval({}, {})'.format(self.start, self.end)
  
  def __eq__(self, other):
    return self.start == other.start and self.end == other.end
  
  def __hash__(self):
    return hash((self.start, self.end))

  @property
  def length(self):
    return self.end - self.start