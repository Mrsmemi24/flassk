# Lista de IPs disponibles

ips_disponibles = [
"192.168.1.10",
"192.168.1.20",
"192.168.1.30",
"192.168.1.40",
"192.168.1.50"
]

# Diccionario de dispositivos

dispositivos = {
101: {
"ip": "192.168.1.10",
"device_name": "Router Principal",
"policy": {
"type": "ALLOW_ALL"
},
"status": "Activo"
},
102: {
"ip": "192.168.1.20",
"device_name": "Switch Piso 1",
"policy": {
"type": "BLOCK_IP",

"blocked_ip": "192.168.1.20"
},
"status": "Activo"
},
103: {
"ip": "192.168.1.30",
"device_name": "Firewall",
"policy": {
"type": "REQUIRED_IP",
"required_ip": "192.168.1.30"
},
"status": "Activo"
},
104: {
"ip": "192.168.1.40",
"device_name": "Servidor Web",
"policy": {
"type": "REQUIRED_IP",
"required_ip": "192.168.1.50"
},
"status": "Inactivo"
},
105: {
"ip": "192.168.1.50",
"device_name": "Access Point",
"policy": {

"type": "ALLOW_ALL"
},
"status": "Activo"
}
}

def mostrar_dispositivos(dispositivos):

for id_dispositivo, dispositivo in dispositivos.items():

print(f"\nID: {id_dispositivo}")
print(f"Nombre: {dispositivo['device_name']}")
print(f"IP: {dispositivo['ip']}")
print(f"Política: {dispositivo['policy']['type']}")
print(f"Estado: {dispositivo['status']}")

resultado = validar_politica(dispositivo)

print(f"Resultado: {resultado}")

def validar_politica(dispositivo):

tipo = dispositivo["policy"]["type"]

if tipo == "ALLOW_ALL":

return "Configuración válida"

elif tipo == "BLOCK_IP":

if dispositivo["ip"] == dispositivo["policy"]["blocked_ip"]:
return "Configuración inválida (IP bloqueada)"

return "Configuración válida"

elif tipo == "REQUIRED_IP":

if dispositivo["ip"] == dispositivo["policy"]["required_ip"]:
return "Configuración válida"

return "Configuración inválida (IP incorrecta)"

return "Política desconocida"

def generar_resumen(dispositivos):

activos = 0
inactivos = 0
validas = 0
invalidas = 0

for dispositivo in dispositivos.values():

if dispositivo["status"] == "Activo":
activos += 1
else: