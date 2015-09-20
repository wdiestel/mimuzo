from sonic import Sonic

class Instrument(Sonic):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.keys = [[0]*cols for i in range(rows)]

    def def_key(self,i,j,code):
        self.keys[i][j]=code

    def play(self,i,j,impuls):
        code = self.keys[i][j]
        self.send_code(code)

