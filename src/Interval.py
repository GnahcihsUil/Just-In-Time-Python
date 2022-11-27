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
  
  def inside_interval(self, x):
    return self.start <= x < self.end

  def pythagorean_triples_in_interval(self):
    triples = []
    for a in range(int(self.start), int(self.end)):
        for b in range(a, int(self.end)):
            c = (a ** 2 + b ** 2) ** 0.5
            if self.inside_interval(c):
                triples.append((a, b, c))
    return triples