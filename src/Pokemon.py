import json


class Pokemon:
    dexId: int  # Número de pokédex
    name: str  # Nombre
    height: int  # Altura
    weight: int  # Peso
    types: []  # Lista de tipos

    def __init__(self, dexId: int, name: str, height: int, weight: int, jsontypes: []):  # Método constructor
        self.dexId = dexId
        self.name = name
        self.height = height
        self.weight = weight
        self.types = []
        for i in range(len(jsontypes)):
            self.types.append((jsontypes[i])["type"]["name"])

    def __str__(self):  # Método equivalente a 'toString' de java (devuelve el objeto como string)
        pokeStr: str = f"NumPkdex:{self.dexId}, Nombre:{self.name}, Altura:{self.height}, Peso:{self.weight}, Tipo{("s", "")[len(self.types) == 1]}:"  # Operador Ternario: Si hay más de un tipo en la lista, añade una s
        for i in range(len(self.types)):   # For que añade los tipos al string
            pokeStr += f"{self.types[i]}"
            if i != len(self.types) - 1:
                pokeStr += "/"  # Si hay algún tipo a continuación, añade la barra
        return pokeStr
