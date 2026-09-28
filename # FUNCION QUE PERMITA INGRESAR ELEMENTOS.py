# FUNCION QUE PERMITA INGRESAR ELEMENTOS EN UNA LISTA DENTRO DEL CICLO FOR
def ingresar():
    elements = []
    for i in range(3):
        dato = input("Ingrese un elemento: ")
        elements.append(dato)
    return elements

# FUNCION QUE IMPRIMA TODOS LOS ELEMENTOS DE UNA LISTA Y UN DICCIONARIO DENTRO DE UN CICLO FOR
def imprimir(lista, diccionario):
    print("\n--- Elementos de la lista ---")
    for i in range(len(lista)):
        print("Elemento:", lista[i])

    print("\n--- Elementos del diccionario net_config ---")
    for key in diccionario:
        print(key, "=", diccionario[key])


# ==========================================
# AQUÍ SE EJECUTA EL CÓDIGO
# ==========================================

# 1. Tu diccionario predefinido (ya tiene los datos, no necesitamos llenarlo)
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

print("\nPASO 2: MOSTRAR LOS DATOS")
# Le pasamos la lista que acabas de llenar y tu diccionario net_config directamente
imprimir(mi_lista, net_config)