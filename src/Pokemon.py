import json

class Pokemon:
    dexId:int
    name:str
    height:int
    weight:int
    types:[]
    def __init__(self,dexId:int,name:str,height:int,weight:int,jsontypes:[]):
        self.dexId=dexId
        self.name=name
        self.height=height
        self.weight=weight
        self.types=[]
        for type in jsontypes:
            tJson = json.loads(type)
            self.types.append((tJson["type"])["name"])
    def __str__(self):
        pokeStr:str = f"NumPkdex:{self.dexId}, Nombre:{self.name}, Altura:{self.height}, Peso:{self.weight}, Tipos:"
        for i in range(len(self.types)):
            pokeStr += f"{self.types[i]}"
            if i != len(self.types)-1:
                pokeStr += "/"
        return pokeStr