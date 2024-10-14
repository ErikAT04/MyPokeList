class Region:
    id: int  # Id de región
    name: str  # Nombre de la región
    lastPoke: int  # Primer pokémon de su pokédex
    firstPoke: int  # Último pokémon de su pokédex

    def __init__(self, id, name, firstPoke, lastPoke): # Método constructor
        self.id = id
        self.name = name
        self.lastPoke = lastPoke
        self.firstPoke = firstPoke
