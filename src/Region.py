class Region:
    id:int
    name:str
    numPkmn:int
    firstPoke:int
    def __init__(self,id,name,numPkmn):
        self.id = id
        self.name = name
        self.numPkmn = numPkmn
        self.firstPoke = 1