import spot
from observ import Observable

mirror = 1

class Field(Observable):

    def __init__(self,screen,rows,cols,width,height,color):
        Observable.__init__(self)
        self.rows = rows
        self.cols = cols
        self.matrix = [[0]*cols for i in range(rows)]
        for r in range(0,rows):
            for c in range(0,cols):
                makulo = spot.Spot(width/cols,height/rows,(width/cols*c,height/rows*r),color,0)
                self.matrix[r][c] = makulo
                makulo.subscribe(self.discharge)
                makulo.draw()
                makulo.blit(screen)

    def setValue(self,row,col,value):
        self.matrix[row][col].setValue(value)


    def blit(self,screen):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                #self.matrix[r][c].draw()
                self.matrix[r][c].blit(screen)

    def charge(self,row,col,cvalue):
        spot = self.matrix[row][col]
        spot.setValue(spot.value + cvalue)

    def charge_all(self,values):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                #self.matrix[r][c].draw()
                spot = self.matrix[r][c]
                if values[c][r] > 50:
                    spot.setValue(spot.value + values[c][r]/255)

    def prop_(self,row,col,val):
        if row>=0 and col>=0 and row<self.rows and col<self.cols:
           spot = self.matrix[row][col]
           spot.add(val)

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

    def is_corner(self,row,col):
        return (
           row==0 and col==0 or
           row==0 and col==self.cols-1 or
           row==self.rows-1 and col==0 or
           row==self.rows-1 and col==self.cols-1)

    def is_edge(self,row,col):
        return (
            not self.is_corner(row,col) and
            row==0 or col==0 or col==self.cols-1 or row==self.rows-1)#

    # ne perdu energion che la rando, sed reflektu ghin
    def propagate_mirror(self,row,col):
        if self.is_corner(row,col):
            pval = self.matrix[row][col].value/3
        elif self.is_edge(row,col):
            pval = self.matrix[row][col].value/5
        else:
            pval = self.matrix[row][col].value/8
        self.prop_to_neigh(row,col,pval)

    # ne reflektighu che la rando sed perdu tie energion    
    def propagate_cease(self,row,col):
        pval = self.matrix[row][col].value/8
        self.prop_to_neigh(row,col,pval)

    def propagate_all(self):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                if mirror:
                    self.propagate_mirror(r,c)
                else:
                    self.propagate_cease(r,c)
        
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                self.matrix[r][c].update(r,c) # update 

    def dump(self):
        #print("------------------------------------")
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                print(str(self.matrix[r][c].value) + " "),
            print()
        print("------------------------------------")

    def discharge(self,event):
        self.fire(event=event)
        #{name: "play", row: r, col: c, impuls: 1.0})
