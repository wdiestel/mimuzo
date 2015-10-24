import spot
from field import Field

discharge = 0.01 # kiom da energio neuzata malaperas chiucikle

class StaticField(Field):

  # ne transdonas energion, sed perdas iom da energio chiuloke
  def propagate_all(self):
      for r in range(0,self.rows):
          for c in range(0,self.cols):
              makulo = self.matrix[r][c]
              makulo.add(-discharge)
              makulo.update(r,c) # update 
