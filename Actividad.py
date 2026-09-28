# FUNCION QUE PERMITA INGRESAR ELEMENTOS EN UNA LISTA DENTRO DEL CICLO FOR
def ingresar():
    '''
    ingresar | Emiliano | 11/09/2026

    Modified:
        11/09/2026 | Initial version | Emiliano
    
    Params:
        Ninguno
    Return: 
        list (Una lista con los elementos ingresados)
    '''
    elements = []
    for i in range(3):
        dato = input("Ingrese un elemento: ")
        elements.append(dato)
    return elements


# FUNCION QUE PERMITA INGRESAR ELEMENTOS A UN DICCIONARIO DENTRO DEL CICLO FOR
def crear_diccionario():
    '''
    crear_diccionario | Emiliano | 11/09/2026

    Modified:
        11/09/2026 | Initial version | Emiliano
    
    Params:
        Ninguno
    Return: 
        dict (Un diccionario con las claves y valores ingresados)
    '''
    diccionario_nuevo = {}
    for i in range(3):
        key = input("Ingrese la clave: ")
        value = input("Ingrese el valor: ")
        diccionario_nuevo[key] = value
    return diccionario_nuevo


# FUNCION QUE IMPRIMA TODOS LOS ELEMENTOS DE UNA LISTA Y UN DICCIONARIO DENTRO DE UN CICLO FOR
def imprimir(lista, diccionario):
    '''
    imprimir | Emiliano | 11/09/2026

    Modified:
        11/09/2026 | Initial version | Emiliano
    
    Params:
        lista (list): La lista que se va a imprimir
        diccionario (dict): El diccionario que se va a imprimir
    Return: 
        None (No devuelve datos, solo imprime en pantalla)
    '''
    print("\n--- Elementos de la lista ---")
    for i in range(len(lista)):
        print("Elemento:", lista[i])

    print("\n--- Elementos del diccionario ---")
    for key in diccionario:
        print(key, "=", diccionario[key])


# AQUÍ SE EJECUTA EL CÓDIGO

net_config = {
    "001" : {
        "ip" : "192.168.0.1",
        "device" : "Router",
        "policy" : "Allow all",
        "Status" : True,
        "lista" : [1,4,6,0,3]
        },
     "002" : {
            "ip": "192.168.0.1",
            "device" : "Firewall",
            "policy" : "Avoid .2 .3. 4",
            "Status" : True
        },
        "003" : {
            "ip": "192.168.0.3",
            "device" : "Server",
            "policy" : "Allow all",
            "Status" : True
        },
        "004" : {
            "ip": "192.168.0.4",
            "device" : "Workstation",
            "policy" : "Deny all",
            "Status" : False
        },
        "005" : {
            "ip": "192.168.0.5",
            "device" : "Database",
            "policy" : ["Ro0","Not Allowed", [0.2,0.3,0.5]],
            "Status" : True
        }
}

print("PASO 1: LLENAR LA LISTA")
mi_lista = ingresar()

print("\nPASO 2: LLENAR UN DICCIONARIO NUEVO (Para cumplir la instrucción)")
mi_dicc_manual = crear_diccionario()

print("\nPASO 3: MOSTRAR LOS DATOS (Lista nueva + Tu diccionario net_config)")
imprimir(mi_lista, net_config)