import spot
from field import Field

mirror = 1 # rejhetu energion che la rando au perdu ghin?
damping = 0.4 # kiom rapide energio estas transdonata al najbaroj, 1.0 rapide, 0 neniom
discharge = 0.1 # kiom da energio neuzata malaperas chiucikle

class DynamicField(Field):

    def prop_(self,row,col,val):
        if row>=0 and col>=0 and row<self.rows and col<self.cols:
           spot = self.matrix[row][col]
           spot.add(val - discharge)

    def prop_2(self,row,col,val,prop):
        if row>=0 and col>=0 and row<self.rows and col<self.cols:
           spot = self.matrix[row][col]
           pval = (val - spot.value)/prop * damping - discharge
           if pval > 0:
               spot.add(pval)
               return pval
        return 0

    def prop_to_neigh(self,row,col,pval):
        self.prop_(row-1,col-1,pval)
        self.prop_(row-1,col,pval)
        self.prop_(row-1,col+1,pval)
        self.prop_(row,col-1,pval)
        self.prop_(row,col+1,pval)
        self.prop_(row+1,col-1,pval)
        self.prop_(row+1,col,pval)
        self.prop_(row+1,col+1,pval)
        self.matrix[row][col].value = 0

    def prop_to_neigh_2(self,row,col,prop):
        val = self.matrix[row][col].value
        v = val
        v -= self.prop_2(row-1,col-1,val,prop)
        v -= self.prop_2(row-1,col,val,prop)
        v -= self.prop_2(row-1,col+1,val,prop)
        v -= self.prop_2(row,col-1,val,prop)
        v -= self.prop_2(row,col+1,val,prop)
        v -= self.prop_2(row+1,col-1,val,prop)
        v -= self.prop_2(row+1,col,val,prop)
        v -= self.prop_2(row+1,col+1,val,prop)
        self.matrix[row][col].value = v 

    # ne perdu energion che la rando, sed reflektu ghin
    def propagate_mirror(self,row,col):
        if self.is_corner(row,col):
            pval = self.matrix[row][col].value/3
        elif self.is_edge(row,col):
            pval = self.matrix[row][col].value/5
        else:
            pval = self.matrix[row][col].value/8
        self.prop_to_neigh(row,col,pval)

    # ne perdu energion che la rando, sed reflektu ghin
    def propagate_mirror_2(self,row,col):
        if self.is_corner(row,col):
            prop=3
        elif self.is_edge(row,col):
            prop = 5
        else:
            prop = 8
        self.prop_to_neigh_2(row,col,prop)

    # ne reflektighu che la rando sed perdu tie energion    
    def propagate_cease(self,row,col):
        pval = self.matrix[row][col].value/8
        self.prop_to_neigh(row,col,pval)

   # ne reflektighu che la rando sed perdu tie energion    
    def propagate_cease_2(self,row,col):
        self.prop_to_neigh(row,col,8)

    def propagate_all(self):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                if mirror:
                    self.propagate_mirror_2(r,c)
                else:
                    self.propagate_cease_2(r,c)
        
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                self.matrix[r][c].update(r,c) # update 

