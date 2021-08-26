import json

import hashlib
BASE_DE_DATOS = "db.json"

# Restricciones de escritura en la base de datos
BASIC_STRUCTURE = {
    "Name":[50,],
    "Age": [2,],
    "Genre": [1,],
    "Phone_number": [15,],
}


def generate_hash(text):
    # funcion encargada de generar un hash en base a un texto dado
    hash = hashlib.sha256(text.encode())
    return hash.hexdigest()


def generate_structure():
    # Restriccion de la longitud de los datos
    BASIC_STRUCTURE["hash"] = [64,]


def verify_db_structure(data):

    # cuando se vaya a escribir un diccionario en el archivo debe seguir una estructura para poder facilitar
    # la busqueda posteriormente, de lo contrario será una estructura json desordenada, en donde la tarea de 
    # buscar será complicada, por no decir imposible

    if data.keys() != BASIC_STRUCTURE.keys():
        raise ValueError("los campos del registro a insertar no son iguales a los de la estructura base")


def verify_field_structure(data, field_name):
    # verificacion de los datos

    if len(str(data)) > BASIC_STRUCTURE[field_name][0]:
        # verificación del tamaño máximo de los datos de cada campo
        raise ValueError("el tamaño maximo de {} es de {} caracteres".format(field_name, BASIC_STRUCTURE[field_name][0]))


def verificar_duplicados(data):
    with open(BASE_DE_DATOS, "r") as f:
            to_write = json.load(f)
            resultados = list(filter(lambda x: x["hash"] == data["hash"], to_write))
            return resultados

def read_json():
    with open(BASE_DE_DATOS) as f:
        data = json.load(f)
        return data

def delete(hash):
    resultado = busqueda(hash, "hash")
    if resultado:
        listado = read_json()
        lugar_lista = listado.index(resultado[0])
        listado.pop(lugar_lista)
        nuclear_write(listado)

def update(data, hash):
    data_hash = generate_hash(str(data))
    data["hash"] = data_hash
    resultado = busqueda(hash, "hash")
    if resultado:
        listado = read_json()
        lugar_lista = listado.index(resultado[0])
        print(lugar_lista)
        listado[lugar_lista] = data
        print(listado[lugar_lista], data)
        nuclear_write(listado)
        
def nuclear_write(data):
    with open(BASE_DE_DATOS, "w") as f:
            data_write = json.dumps(data)
            f.write(data_write)

def write_json(data):
    # genera un id unico para cada registro en base a hashes
    data["hash"] = generate_hash(str(data))
    verify_db_structure(data)

    for key in BASIC_STRUCTURE:
        verify_field_structure(data[key], key)

    try:

        # si el json existe
        with open(BASE_DE_DATOS, "r") as f:
            to_write = json.load(f)
            if verificar_duplicados(data):
                raise ValueError("este registro ya existe en la base de datos")

        to_write.append(data)

        with open(BASE_DE_DATOS, "w") as f:
            data_write = json.dumps(to_write)
            f.write(data_write)

    except (FileNotFoundError, json.JSONDecodeError) as e:

        # asumiendo que el json no existe
        with open(BASE_DE_DATOS, "w") as f:
            start_list = []
            start_list.append(data)
            to_write = json.dumps(start_list)
            f.write(to_write)

def busqueda(keyword ,field):
    listado = read_json()
    resultado = list(filter(lambda x: keyword in str(x[field]) or keyword == str(x[field]), listado))
    if not resultado:
        raise ValueError("no se enconstraron resultados para {} en el campo {}".format(keyword, field))
    
    return resultado

def print_bd():
    listado = read_json()
    for item in listado:
        print("Nombre Completo: ", item["Name"])
        print("Genero:", item["Genre"])
        print("Edad: ", item["Age"])
        print("Telefono: ", item["Phone_number"], "\n")

def main():
    # lo que ocupa está funcion es crear el campo hash al diccionario que se escribirá en el json
    generate_structure()
    #update({"Name":"Augusto Carrillo","Age":25, "Genre":"F","Phone_number":"5555565",}, "1a165e75a7d368496e0e2a52843b7c9c7545d5df282487132a3ebb39ce70d3cf")
    #update({"Name":"Augusto Carrillo","Age":55, "Genre":"F","Phone_number":"5555565",}, "5a4c08b8800e44ae5ce72b30e5bbf479075764f370fbcf17cb818b901b977185")
    #delete("5a4c08b8800e44ae5ce72b30e5bbf479075764f370fbcf17cb818b901b977185")
    #write_json({"Name":"Augusto Carrillo","Age":39, "Genre":"M","Phone_number":"5555565",})

    print("Bienvenido al sistema de agendas\n")
    print_bd()
    print("--para insertar un registro ingrese 1\n")
    print("--para eliminar un registro ingrese 2\n")
    print("--para Actualizar un registro ingrese 3\n")
    print("--para Salir ingrese n\n")
    
    


if __name__ == "__main__":
    # este condicional evita que cuando se importe un modulo a otro archivo .py se ejecute lo que 
    # se llame o instancie aquí.
    main()
