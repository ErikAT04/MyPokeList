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