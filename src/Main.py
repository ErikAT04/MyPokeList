import os
from logging import fatal

import requests

from src.Pokemon import Pokemon
from src.Region import Region

pokeList = [] #Lista que guarda los pokemon
regionList = [] #Lista que guarda las regiones
myList = [] #Lista los pokémon que hay guardados en la lista personalizada
myPokeFile = "myPokeList.txt"
i = 1 #Inicializo un incrementador

def initLists():
    pokeList.append(Pokemon(0, "Missingno", 0, 0, ["null"]))
    print("Iniciando datos, por favor, espere...")
    statuscode = 200 #Inicia el código de estado como 200 para poder entrar en el bucle
    i = 1
    while statuscode == 200:
        pokeSearch = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(i))
        statuscode = pokeSearch.status_code #Guarda el código de estado de la nueva búsqueda
        if statuscode == 200: #Si es 200 (se ha realizado correctamente la conexión)
            jsonSearch=pokeSearch.json() #Guarda el archivo json como biblioteca
            pokemon:Pokemon = Pokemon(jsonSearch["id"], jsonSearch["name"], jsonSearch["height"], jsonSearch["weight"], jsonSearch["types type name"]) #Guarda los datos así
            pokeList.append(pokemon)
            print(pokemon.types)
    statuscode = 200
    i=1
    while statuscode == 200:
        regionSearch = requests.get("https://pokeapi.co/api/v2/region/"+str(i))
        statuscode = regionSearch.status_code
        if statuscode == 200:
            jsonSearch=regionSearch.json()
            numPkmn = jsonSearch["pokemon_entries"].size() # Cojo el tamaño de la lista de las entradas de la pokedex de cada región
            region:Region = Region(jsonSearch["id"], jsonSearch["name"], numPkmn)
            regionList.append(region)
            if len(regionList)>2:
                regionList[len(regionList)-1].firstPoke = regionList[len(regionList)-2].firstPoke + regionList[len(regionList)-2].numPkmn
    try:
        with open(myPokeFile, "r") as myFile:
            for pokemon in pokeList: #Por cada pokémon en la lista principal:
                if pokemon.name in myFile: #Si el nombre del pokémon aparece en el archivo, se añade a la lista personalizada
                    myList.append(pokemon)
    except FileNotFoundError: #Si al intentar abrir el archivo, no lo encuentra:
        print("No se ha encontrado el archivo personal, se va a crear ahora:")
        with open(myPokeFile, "w") as myFile: #Al hacer esto, si no encuentra un archivo, lo crea
            print("Archivo creado")


initLists()
opt:int = 1


def addToList():
    pokemonIdent = input("Escribe el nombre o id del pokémon: ")
    isAlready:bool = False
    for pokemon in myList:
        if (pokemonIdent.isdigit() and pokemonIdent == pokemon.dexId) or (pokemonIdent == pokemon.name):
            isAlready = True
    if not isAlready:
        for pokemon in pokeList:
            if pokemonIdent == pokemon.dexId or pokemonIdent == pokemon.name:
                myList.append(pokemon)
                isAlready = True
                print("Añadido")
        if not isAlready:
            print("No existe ese pokémon")
    else:
        print("Ese pokémon ya estaba en la lista")

def allPokeNames()->str:
    allNames:str = "Todos los pokémon: "
    for i in range(len(pokeList)):
        allNames = allNames + pokeList[i].name
        if i<len(pokeList)-1:
            allNames = allNames + ", "
    return allNames

def seeOneRegion():
    reg = input("Escribe el nombre o id de la región (0 = Regional, 1 = Kanto, 2 = Johto...")
    for region in regionList:
        if (reg.isdigit() and reg == region.id) or (reg.isalpha() and reg.lower() == region.name):
            print(f"Mostrando pokédex de {region.name.capitalize()}:")
            for i in range(region.firstPoke), (region.numPkmn + region.firstPoke):
                print(pokeList[i])
        else:
            print("Región no encontrada")


def quitFromList():


def dropList():
    pass


while opt != 0 and opt != 6: #Si ni se borra el archivo ni si se sale del programa:
    try:
        opt = int(input("Escribe una opción: \n1.Añadir pokémon a la lista\n2.Ver mi lista\n3.Ver todos los nombres de pokémon actuales\n4.Ver pokémon de una sola región\n5.Quitar un pokémon de mi lista\n6.Borrar mi lista\n0.Salir"))
        match opt:
            case 1: addToList()
            case 2: print(myList)
            case 3: print(allPokeNames())
            case 4: seeOneRegion()
            case 5: quitFromList()
            case 6: dropList()
            case 0: print("Terminando programa...")
            case _: print("Opción no válida")

    except ValueError:
        print("Opción no válida")
        opt = 1
    finally:
        print()