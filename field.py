import spot
from observ import Observable

# mirror = 1 # rejhetu energion che la rando au perdu ghin?
threshold = 5 # ju pli granda, des pli fortaj movoj necesas por shargi
charge_factor = 0.4 # kiom da energio movado enmetas en la energikampon
# damping = 0.4 # kiom rapide energio estas transdonata al najbaroj, 1.0 rapide, 0 neniom
# discharge = 0.1 # kiom da energio neuzata malaperas chiucikle

class Field(Observable):

    def __init__(self,screen,rows,cols,width,height,color):
        Observable.__init__(self)
        self.rows = rows
        self.cols = cols
        self.matrix = [[0]*cols for i in range(rows)]
        for r in range(0,rows):
            for c in range(0,cols):
                makulo = spot.Spot(screen,width/cols,height/rows,(width/cols*c,height/rows*r),color,0)
                self.matrix[r][c] = makulo
                makulo.subscribe(self.onEvent)
                makulo.draw()
                makulo.blit(screen)

    def setValue(self,row,col,value):
        self.matrix[row][col].setValue(value)


    def blit(self,screen):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                #self.matrix[r][c].draw()
                self.matrix[r][c].blit(screen)

    # chargas unuopan makulon
    def charge(self,row,col,cvalue):
        spot = self.matrix[row][col]
        spot.setValue(spot.value + cvalue)

    # transprenas por chiu makulo de valormatrico, ekz. de kameramovado
    def charge_all(self,values):
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                #self.matrix[r][c].draw()
                spot = self.matrix[r][c]
                if values[c][r] > threshold:
                    spot.setValue(spot.value + values[c][r]/255*charge_factor)

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

    # ne shanghas la energione la makuloj, sed ekz. DynamicField transdonas tiel energion al najbaraj makuloj
    def propagate_all(self):
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

    def onEvent(self,event):
        self.fire(event=event)
        #{name: "play", row: r, col: c, impuls: 1.0})
