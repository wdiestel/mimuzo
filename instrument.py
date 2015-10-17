from sonic import Sonic

class Instrument(Sonic):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.keys = [[0]*cols for i in range(rows)]
        self.mods = [[0]*cols for i in range(rows)]

    def def_key(self,i,j,code):
        self.keys[i][j]=code

    def def_mod(self,i,j,code):
        self.mods[i][j]=code

    def play(self,i,j,impuls):
        code = self.keys[i][j]
        cmd = code.format(impuls)
        self.send_code(cmd)

    def modify(self,i,j,value):
        code = self.mods[i][j]
        cmd = code.format(value)
        self.send_code(cmd)
