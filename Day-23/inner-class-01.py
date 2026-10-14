class Outer:
  def __init__(self):
    self.name = "Outer Class"

  class Inner:
    def __init__(self):
      self.name = "Inner Class"

    def display(self):
      return "This is the inner class"


	
    
outer = Outer()
inner = Outer.Inner()

print(outer.name)
print(inner.name)
print(inner.display())