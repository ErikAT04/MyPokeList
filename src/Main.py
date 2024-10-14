import json
import os
import requests
from src.Pokemon import Pokemon  # Importo un archivo existente
from src.Region import Region

pokeList = []  # Lista que guarda los pokemon
regionList = []  # Lista que guarda las regiones
myList = []  # Lista que muestra los pokémon que hay guardados en la lista personalizada
listTypes = []  # Lista que guarda todos los tipos
myPokeFile = "myPokeList.txt"  # Dirección del fichero
i = 1  # Inicializo un incrementador


def initLists():  # Función que se inicia al principio del programa: Inicia las listas y prepara el archivo de la lista personalizada
    pokeList.append(Pokemon(0, "Missingno", 0, 0, [
        {"type": {"name": "null"}}]))  # Introduzco a MissingNo, un pokémon "no oficial" que no aparece en el api
    print("Iniciando datos, por favor, espere unos minutos...")
    statuscode = 200  # Inicia el código de estado como 200 para poder entrar en el bucle
    i = 1  # Inicia el iterador en 1, cogiendo el primer pokémon de la dex
    print(
        "Cargando datos, espere al nombre del último pokémon:")  # Más bien orientativo, para que el usuario sepa por dónde llega la carga
    while statuscode == 200:  # Para empezar: Mientras se encuentren siempre datos (El código de estado sea 200):
        pokeSearch = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(
            i))  # Hace una búsqueda en el pokémon cuyo número de la pokedex es el iterador
        statuscode = pokeSearch.status_code  # Guarda el código de estado de la nueva búsqueda
        if statuscode == 200:  # Si es 200 (se ha realizado correctamente la conexión)
            jsonSearch = pokeSearch.json()  # Guarda el archivo json como biblioteca
            pokemon: Pokemon = Pokemon(jsonSearch["id"], jsonSearch["name"], jsonSearch["height"], jsonSearch["weight"],
                                       jsonSearch[
                                           "types"])  # Guarda los datos que nos interesan en un objeto de tipo Pokemon
            pokeList.append(pokemon)  # Introduce el pokémon en una de las listas
            i += 1  # Añade 1 al iterador y pasa al siguiente
            print(pokemon.name, end=", ")  # Imprime el pokémon y añade un punto y coma para el próximo
    print("")  # Salto de línea, mera estética
    pokeSearch = requests.get(
        "https://pokeapi.co/api/v2/type/")  # Hace ahora una búsqueda de los tipos registrados en el api
    statuscode = pokeSearch.status_code  # Guarda el código de estado y si es 200 sigue operando
    if statuscode == 200:
        jsonSearch = pokeSearch.json()  # Guarda la información en un objeto json
        results = jsonSearch["results"]  # Sacamos del json la lista de resultados (donde se guardan todos los tipos)
        for result in results:  # Por cada resultado, nos quedamos solo con el nombre
            listTypes.append(result["name"])  # Se añade el nombre a la lista de tipos
    try:  # Inicio del control de excepciones
        with open("regionlist.json",
                  "r") as regionListFile:  # Se abre el archivo json de la lista de regiones (La API no daba la información que buscaba)
            listJson = json.load(regionListFile)  # Se hace una lista con la información dada en el json
            for s in listJson:  # Por cada elemento json de la lista se crea una región y se añade a la lista de Python
                reg: Region = Region(s["id"], s["region"], s["firstPoke"], s["lastPoke"])
                regionList.append(reg)
        with open(myPokeFile, "r") as myFile:  # Se abre el archivo personalizado en modo lectura
            listAux = []  # Crea una lista auxiliar donde guarda únicamente los nombres de la lista
            for line in myFile:  # Por cada linea en el archivo, guarda el nombre en la lista
                listAux.append(
                    line[0:len(line) - 1])  # Quito el salto de linea (\n) que tiene el fichero guardado en cada uno
            for pokemon in pokeList:  # Por cada pokémon en la lista principal:
                if pokemon.name in listAux:  # Si el nombre del pokémon aparece en el archivo, se añade a la lista personalizada
                    myList.append(pokemon)
    except FileNotFoundError:  # Si al intentar abrir el archivo personalizado, no lo encuentra:
        print("No se ha encontrado el archivo personal, se va a crear ahora:")
        with open(myPokeFile, "w"):  # Al hacer esto, si no encuentra un archivo, lo crea
            print("Archivo creado")


def addToList():  # Función encargada de guardar en la lista personalizada el pokémon que nos interese
    pokemonIdent = input("Escribe el nombre o id del pokémon: ")  # Guarda o el nombre o el id
    isAlready: bool = False  # Semáforo que marca si ya estaba guardado o si se ha guardado el pokémon
    for pokemon in myList:  # ForEach de la lista de pokémon personalizada
        if (pokemonIdent.isdigit() and int(pokemonIdent) == pokemon.dexId) or (pokemonIdent.lower() == pokemon.name):
            isAlready = True  # Si el id (solo digitos) es igual al id de un pokémon de la lista o el nombre (minúsculas) es igual al nombre de un pokemon de la lista, la booleana es true
    if not isAlready:  # Si en este momento la booleana sigue siendo true (no ha aparecido el pokémon en la lista):
        for pokemon in pokeList:  # Recorre esta vez la lista de pokemon general en un forEach
            if (pokemonIdent.isdigit() and int(
                    pokemonIdent) == pokemon.dexId) or pokemonIdent.lower() == pokemon.name:  # Si el nombre o id cumple la condición de antes:
                myList.append(pokemon)  # Añade la instancia actual del ForEach a la lista personalizada
                isAlready = True  # Reutiliza isAlready y lo convierte en true
                print(f"{pokemon.name} añadido correctamente")  # Avisa al usuario
                with open(myPokeFile, "a") as myFile:  # Abre el fichero de la lista personalizada y escribe su nombre
                    myFile.write(pokemon.name + "\n")
        if not isAlready:  # Si no se ha editado esta segunda vez, da por hecho que el pokémon no existe (ya que no existe en la API)
            print("No existe ese pokémon")
    else:  # Si entró en el primer bucle e isAlready era True, el pokémon estaba en la lista, por lo que no se podía añadir.
        print("Ese pokémon ya estaba en la lista")


def allPokeNames() -> str:  # Función que muestra los nombres de todos los pokémon del api
    allNames: str = "Todos los pokémon: \n"  # Inicio del String
    for i in range(len(pokeList)):  # Recorre la lista entera de pokemon
        allNames = allNames + pokeList[
            i].name  # Añade al final del string el nombre del pokémon de la instancia en ese momento
        if i < len(
                pokeList) - 1:  # Por estética, si el iterador no ha llegado al final de la lista, añade una coma y un espacio
            allNames = allNames + ", "
    return allNames  # Devuelve el String


def seeOneRegion():  # Función que muestra todos los pokémon de la lista del api de la región que diga el usuario
    reg = input(
        "Escribe el nombre o id de la región (1 = Kanto, 2 = Johto...): ")  # Guarda el id o el nombre de la región
    regionFound: bool = False  # Crea una booleana que controla si se encuentra o no la región
    for region in regionList:  # Recorre la lista de regiones para verificar si la región puesta existe
        if (reg.isdigit() and int(reg) == region.id) or (
                reg.lower() == region.name):  # Si el valor introducido es de digitos y es igual al id, o si es igual al nombre de la región (minúsculas):
            regionFound = True  # La booleana se vuelve true
            print(f"Mostrando pokédex de {region.name.capitalize()}:")
            for i in range(region.firstPoke, (
                    region.lastPoke + 1)):  # Entra en el rango del primer y último pokémon de la región e imprime todos los pokémon de la lista
                print(pokeList[i])  # Imprime por pantalla los pokémon que entren en la instancia descrita por la región
    if not regionFound:  # Si la región no se ha encontrado, avisa al usuario
        print("No existe esa región")


def quitFromList():  # Función que borra los pokémon de la lista puesta
    poke = input("Escribe el nombre o el id del pokémon a borrar de tu lista: ")  # Guarda el nombre o id del pokémon
    pokemonFound: bool = False  # Booleana que guarda si se ha encontrado el pokémon
    for pokemon in myList:  # Recorre la lista personalizada
        if (poke.isdigit() and pokemon.dexId == int(poke)) or (
                poke.isalpha() and poke.lower() == pokemon.name):  # Si el id (solo digitos) o el nombre (minúsculas) coincide con el de algún pokémon:
            pokemonFound = True  # La booleana cambia a true
            myList.remove(pokemon)  # Borra al pokémon de la lista
            print(f"{pokemon.name} borrado correctamente")  # Avisa al usuario
            with open(myPokeFile,
                      "w") as myFile:  # Abre el fichero de la lista en modo escritura (borra lo que hubiera en el fichero previamente)
                for pokemon in myList:  # Por cada pokémon en la lista personalizada, añade su nombre y salta de línea
                    myFile.write(pokemon.name + "\n")
    if not pokemonFound:  # Si no encuentra al pokémon avisa al usuario
        print("No se ha encontrado al pokémon")


def dropList():  # Función que borra toda la lista en un moménto
    try:
        os.remove(myPokeFile)  # Con el comando os.remove(nombre) borra completamente el archivo
        print("Lista borrada")
    except FileNotFoundError:  # De no encontrarlo, salta la excepción
        print("Ha habido un error con el borrado")


def filter(fun,
           passedList) -> []:  # Función DE ORDEN SUPERIOR que devuelve una lista filtrada según qué función reciba de parámetro
    filteredList = []  # Crea la lista vacía
    for pokemon in passedList:  # Recorre los pokemon de la lista pasada
        if fun(pokemon):  # La función aquí se puede ver que devuelve una booleana. En caso de que la booleana sea cierta, añade al pokémon a la lista
            filteredList.append(pokemon)
    return filteredList  # Devuelve la lista filtrada


def criteriaSearch():  # Función que pide al usuario un criterio de filtro a seguir
    opt = 1  # Inicia la variable de opción para que entre en el bucle
    while not (opt <= 0 or opt > 3):  # Mientras la variable no sea ni menor o igual a 0 ni mayor a 3 (entre 1 y 3)
        try:  # Abre el control de excepciones
            opt = int(input(
                "Elige una opción:\n1. Por tipo\n2.Por rango de números de pokédex\n3. Por caracteres en el nombre\n0. Salir\nOpción: "))
            filteredPokeList = []  # Crea una lista vacía
            match opt:  # Switch en función de la opción
                case 1:  # Si se ha elegido filtrar por tipo:
                    pokeType = input("Escribe el tipo: ")  # Pide al usuario introducir un tipo (en inglés)
                    typeFound: bool = False  # Inicia una booleana que comprueba si se ha encontrado el tipo
                    for t in listTypes:  # Recorre la lista de tipos
                        if pokeType.lower() == t.lower():  # Si coincide que el tipo escrito existe en la lista:
                            typeFound = True  # La booleana se vuelve true
                            print("Guardando por tipo:")  # Avisa al usuario
                            filteredPokeList = filter(lambda x: t in x.types,
                                                      myList)  # Filtra con una función lambda que solo es true si el tipo escrito se encuentra entre los tipos del pokémon
                    if not typeFound:  # Si no encuentra el tipo avisa al usuario
                        print("No existe ese tipo")
                case 2:  # Si se ha elegido filtrar por rango de valores en la pokédex:
                    num1 = int(input("Escribe un primer número: "))  # Pide dos números por teclado
                    num2 = int(input("Escribe un segundo número: "))
                    if num1 < 0 or num2 < 0 or num1 > len(pokeList) or num2 > len(
                            pokeList):  # Si alguno de ellos se sale del rango de la lista avisa al usuaro
                        print("Alguno de los valores excede los límites")
                    else:  # Si no se da el caso, procede a la siguiente condición
                        if num1 < num2:  # Si el primer número es menor que el segundo, sigue la función correctamente
                            print(
                                f"Preparando lista entre los valores {num1} y {num2}: ")  # Avisa al usuario de que va a filtrar
                            filteredPokeList = filter(lambda x: num1 <= x.dexId <= num2,
                                                      myList)  # Filtra con una función lambda que solo es true si el número de la pokédex se encuentra entre num1 y num2 (incluidos)
                        else:  # Si num2 era menor o igual a num1:
                            print("El primer número debe ser menor que el segundo")
                case 3:  # Si el usuario ha elegido filtrar por caracteres en el nombre:
                    regex = input(
                        "Escribe los caracteres que debe tener el nombre de los pokémon: ")  # Guarda la cadena de caracteres
                    filteredPokeList = filter(lambda x: regex.lower() in x.name.lower(),
                                              myList)  # Filtra con una función lambda que solo es true si el nombre contiene la cadena de caracteres dada
            if len(filteredPokeList) == 0:  # Si, una vez acabado el switch, la lista filtrada no tiene datos (su longitud es 0), avisa al usuario
                print("No se ha realizado la lista")
            else:  # Si tiene datos, muestra la lista
                print("Lista filtrada:")
                for pokemon in filteredPokeList:
                    print(pokemon)
        except ValueError:  # Si el usuario mete un valor no numérico a la opción:
            print("Opción no válida")
            opt = 1  # Iguala opt a 1 para evitar errores en la condición
        finally:
            print()  # Salto de línea, mera estética


def seeMyListInRegions():  # Función muestra los pokémon de la lista personalizada en función de la región a la que pertenecen
    for region in regionList:  # Por cada región registrada:
        print(f"Pokemon de tu lista en la región de {region.name.capitalize()}:")
        for pokemon in myList:  # Por cada pokémon de la lista personalizada:
            if pokemon.dexId in range(region.firstPoke,
                                      region.lastPoke + 1):  # Si el pokémon se encuentra en el rango de la pokédex de la región, se imprime el pokémon
                print(pokemon)
        print(" ")  # Salto de línea


# Ahora sí, se inicia el programa
initLists()  # Comienza iniciando las listas y creando una variable de opción en 5
opt: int = 1
while opt != 0 and opt != 9:  # Si ni se borra el archivo ni si se sale del programa:
    try:  # Control de excepciones
        opt = int(input(
            "Escribe una opción: \n1.Añadir pokémon a la lista\n2.Ver mi lista\n3.Ver todos los nombres de pokémon actuales\n4.Ver pokémon de una sola región\n5.Quitar un pokémon de mi lista\n6.Buscar en mi lista según criterio\n7.Filtrar mi lista según región\n9.Borrar mi lista\n0.Salir\nOpción: "))
        match opt:  # Switch en función de la opción elegida
            case 1:
                addToList()
            case 2:  # No necesita hacer una función a mayores, basta con hacer dos líneas de código
                for pokemon in myList:  # Por cada pokemon de la lista personalizada, lo imprime por pantalla
                    print(pokemon)
            case 3:
                print(allPokeNames())  # La función devuelve un string, por lo que se imprime con print
            case 4:
                seeOneRegion()
            case 5:
                quitFromList()
            case 6:
                criteriaSearch()
            case 7:
                seeMyListInRegions()
            case 9:
                dropList()
            case 0:
                print("Terminando programa...")
            case _:  # Si se introduce una opción inesperada (default de java)
                print("Opción no válida")

    except ValueError:  # Si el usuario introduce un valor no entero
        print("Opción no válida")
        opt = 1  # Opt se iguala a 1 para evitar posibles fallos en el programa
    finally:
        print()  # Salto de línea
