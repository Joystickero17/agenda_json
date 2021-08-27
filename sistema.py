import json
from os import system, name
import hashlib
BASE_DE_DATOS = "db.json"

ACTIONS = (
    ("Insertar", "Insertado(s)",),
    ("Actualizar", "Actualizado(s)")
)

# Restricciones de escritura en la base de datos
BASIC_STRUCTURE = {
    "Name":[50,],
    "Age": [2,],
    "Genre": [1,],
    "Phone_number": [15,],
}

def clear():
    # funcion para borrar datos de la consola
    if name == "nt":
        system("cls")
    else:
        print("\033c",end="")


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
    try:
        with open(BASE_DE_DATOS) as f:
            data = json.load(f)
            return data
    except Exception as e:
        return nuclear_write([])

    
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
            return data_write

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
def print_custom_result(lista):
    
    for index, item in enumerate(lista):
        print("id: ", index)
        print("Nombre Completo: ", item["Name"])
        print("Genero:", item["Genre"])
        print("Edad: ", item["Age"])
        print("Telefono: ", item["Phone_number"], "\n")
    if not lista:
        print("\nNO HAY REGISTROS PARA MOSTRAR, INTENTELO DE NUEVO...\n")

def print_bd():
    listado = read_json()
    for index, item in enumerate(listado):
        print("id: ", index)
        print("Nombre Completo: ", item["Name"])
        print("Genero:", item["Genre"])
        print("Edad: ", item["Age"])
        print("Telefono: ", item["Phone_number"], "\n")
    if not listado:
        print("\nNO HAY REGISTROS PARA MOSTRAR, POR FAVOR INGRESAR ALGUNO...\n")

    return listado
def verify_exit(data):
    
    return list(filter(lambda x: x == "n", data.values()))

def action_records(action, update_data=None):
    verify = True
    while verify:
        clear()
        
        insert_data = dict.fromkeys(BASIC_STRUCTURE.keys())
        if update_data:
            print("datos actuales:\n Nombre: {},\nEdad: {},\nSexo: {},\nTelefono: {}".format(*update_data.values()))
            print("\nACTUALIZAR:\n")
        
        print("para salir introduzca la letra n\n")
        insert_data["Name"] = input("Ingrese el nombre: ")
        if verify_exit(insert_data): 
            break
        insert_data["Age"] = input("Ingrese la Edad: ")
        if verify_exit(insert_data): 
            break
        insert_data["Genre"] = input("Ingrese el Sexo: ")
        if verify_exit(insert_data): 
            break
        insert_data["Phone_number"] = input("Ingrese el numero de teléfono: ")
        if verify_exit(insert_data): 
            break

        if None in insert_data.values():
            clear()
            none_indexes = []
            name_fields = list(insert_data.keys())

            # listando los campos que el usuario dejó vacios
            for index, item in enumerate(insert_data.values()):
                if not item and name_fields[index] != "hash":
                    none_indexes.append(name_fields[index])
            clear()
            

            for field in none_indexes:

                print("Por favor ingrese un valor para los siguientes campos (No pueden estar vacíos): \n",*none_indexes)
                while True:
                    insert_data[field] = input("\ninserte un dato para: "+ field+"  ")
                    if insert_data[field]:
                        break
                    clear()
                    input("datos inválidos intentelo nuevamente...")
        
        while True:
            clear()
            print("los datos a {} son los siguientes:\n".format(ACTIONS[action-1][0]))
            print("Nombre: {}\nEdad:{}\nSexo: {}\nTelefono: {}\n".format(*insert_data.values()))
            inner_choice = input("si estos datos correctos escriba Y, de lo contrario escriba n: ")

            if inner_choice == "Y":
                try:
                    if action == 1:
                        write_json(insert_data)
                    else:
                        update(insert_data, update_data["hash"])
                    clear()
                    input("\n   REGISTRO {} CON ÉXITO, PRESIONE ENTER PARA CONTINUAR...".format(ACTIONS[action-1][1]))
                    verify = False
                    clear()
                    break
                except Exception as e:
                    print(e)
                    input("Presione Enter para continuar...")
                    break
                

            elif inner_choice == "n":
                clear()
                break
            else:
                input("\n\nOpcion incorrecta por favor intentelo de nuevo... \n presione enter para continuar")

def main():
    # lo que ocupa está funcion es crear el campo hash al diccionario que se escribirá en el json
    generate_structure()
    search_results = []
    #update({"Name":"Augusto Carrillo","Age":25, "Genre":"F","Phone_number":"5555565",}, "1a165e75a7d368496e0e2a52843b7c9c7545d5df282487132a3ebb39ce70d3cf")
    #update({"Name":"Augusto Carrillo","Age":55, "Genre":"F","Phone_number":"5555565",}, "5a4c08b8800e44ae5ce72b30e5bbf479075764f370fbcf17cb818b901b977185")
    #delete("5a4c08b8800e44ae5ce72b30e5bbf479075764f370fbcf17cb818b901b977185")
    #write_json({"Name":"Augusto Carrillo","Age":39, "Genre":"M","Phone_number":"5555565",})
    print("Bienvenido al sistema de agendas\n")
    while True:
        if search_results:
            print_custom_result(search_results)
        else:
            listado = print_bd()
            print("--para insertar un registro ingrese 1\n")
        print("--para Actualizar un registro ingrese 2\n")
        print("--para Eliminar un registro ingrese 3\n")

        if search_results:
            print("--para buscar de nuevo ingrese 4\n")
            print("--para ir al principio ingrese 5\n")
        else:    
            print("--para buscar un registro ingrese 4\n")

        print("--para Salir ingrese n\n")
        
        choice = input()

        if choice == '1' and not search_results:
            action_records(int(choice))

        elif choice == '2':
            while True:
                clear()
                if not listado:
                    input("NO EXISTE NINGUN REGISTRO EN LA BASE DE DATOS, POR FAVOR AGREGAR ALGUNO, PRESIONE ENTER PARA CONTINUAR...")
                    clear()
                    break
                elif search_results:
                    listado = search_results    
                    print_custom_result(listado)
                else:
                    listado = print_bd()

                print("Ingrese n para salir al menu principal")
                update_choice = input("\nIngrese el id del registro que quiere modificar acontinuación: ")
                if update_choice.isdigit():
                    update_choice = int(update_choice)
                    if update_choice in range(len(listado)):
                        action_records(int(choice), listado[update_choice])
                    else:
                        input("\n    LA OPCION NO SE ENCUENTRA EN EL RANGO DE LA LISTA, PRESIONE ENTER PARA CONTINUAR...")
                else:
                    clear()
                    if update_choice == "n":
                        break
                    clear()
                    input("\n    LA OPCION TIENE QUE SER NUMERICA, PRESIONE ENTER PARA CONTINUAR...")

        elif choice == "3":
            verify = True
            while verify:
                clear()

                if not listado:
                    input("NO EXISTE NINGUN REGISTRO EN LA BASE DE DATOS, POR FAVOR AGREGAR ALGUNO, PRESIONE ENTER PARA CONTINUAR...")
                    verify = False
                    clear()
                    break
                elif search_results:
                    listado = search_results    
                    print_custom_result(listado)
                else:
                    listado = print_bd()

                print("Ingrese n para salir al menu principal")
                delete_choice = input("\nIngrese el id del registro que quiere ELIMINAR acontinuación: ")
                if delete_choice.isdigit():
                    delete_choice = int(delete_choice)
                    if delete_choice in range(len(listado)):
                        while True:
                            clear()
                            print("los datos a Eliminar son los siguientes:\n")
                            print("Nombre: {}\nEdad:{}\nSexo: {}\nTelefono: {}\n".format(*listado[delete_choice].values()))
                            inner_choice = input("si estos datos correctos escriba Y, de lo contrario escriba n: ")

                            if inner_choice == "Y":
                                try:
                                    delete(listado[delete_choice]["hash"])
                                    clear()
                                    input("\n   REGISTRO ELIMINADO CON ÉXITO, PRESIONE ENTER PARA CONTINUAR...")
                                    verify= False
                                    clear()
                                    break
                                except Exception as e:
                                    print(e)
                                    input("Presione Enter para continuar...")
                                    break
                                

                            elif inner_choice == "n":
                                clear()
                                break
                            else:
                                input("\n\nOpcion incorrecta por favor intentelo de nuevo... \n presione enter para continuar")
                        
                    else:
                        input("\n    LA OPCION NO SE ENCUENTRA EN EL RANGO DE LA LISTA, PRESIONE ENTER PARA CONTINUAR...")
                else:
                    clear()
                    if delete_choice == "n":
                        break
                    clear()
                    input("\n    LA OPCION TIENE QUE SER NUMERICA, PRESIONE ENTER PARA CONTINUAR...")

        elif choice == "4":
            while True:
                clear()
                listado = print_bd()
                if not listado:
                    input("NO EXISTE NINGUN REGISTRO EN LA BASE DE DATOS, POR FAVOR AGREGAR ALGUNO, PRESIONE ENTER PARA CONTINUAR...")
                    clear()
                    break
                clear()
                lista_opciones = list(BASIC_STRUCTURE.keys())

                keyword = input("Ingrese la palabra para buscar en el registro o $ para salir: ")
                if keyword == "$":
                    clear()
                    break
                for index, key in enumerate(lista_opciones):
                    print("\ningrese {} para buscar por {}".format(index, key))
                
                search_choice = input("- ")

                if search_choice.isdigit():
                    search_choice = int(search_choice)
                    try:
                        search_results = busqueda(keyword, lista_opciones[search_choice])
                        clear()
                        break
                    except Exception as e:
                        print(e)
                        input("\nPRESIONE ENTER PARA CONTINUAR...")
                else:
                    clear()
                    if delete_choice == "n":
                        break
                    clear()
                    input("\n    LA OPCION TIENE QUE SER NUMERICA, PRESIONE ENTER PARA CONTINUAR...")

        elif choice == "5":
            clear()
            search_results = []
            continue

        elif choice == "n":
            break

        else:
            print("la opción ingresada no es valida")
            input("presione enter para continuar")

    

main()