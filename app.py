import json
from flask import Flask, jsonify


app = Flask(__name__)


with open("API.json", "r") as json_file:
    datos_json = json.load(json_file)




@app.route("/")
def index():
    return """
    <html>
    <body>
        <h1>Hola mundo</h1>
        <a href="/json/3D:RF:09:7F::">Buscar Datos</a>
    </body>
    </html>
    """


DISPOSITIVOS = {


    "101": {


        "ip": "192.168.1.10",


        "device_name": "Router Principal",


        "policy": {"type": "ALLOW_ALL"},


        "status": "Activo",


    },


    "102": {


        "ip": "192.168.1.20",


        "device_name": "Switch Piso 1",


        "policy": {"type": "BLOCK_IP", "blocked_ip": "192.168.1.20"},


        "status": "Activo",


    },


    "103": {


        "ip": "192.168.1.30",


        "device_name": "Firewall",


        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.30"},


        "status": "Activo",


    },


    "104": {


        "ip": "192.168.1.40",


        "device_name": "Servidor Web",


        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.50"},


        "status": "Activo",


    },


    "105": {


        "ip": "192.168.1.50",


        "device_name": "Access Point",


        "policy": {"type": "ALLOW_ALL"},


        "status": "Activo",


    },


        "106": {


        "ip": "192.168.1.60",


        "device_name": "Servidor de Base de Datos",


        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.60"},


        "status": "Activo",


    },


    "107": {


        "ip": "192.168.1.70",


        "device_name": "Cámara IP Entrada",


        "policy": {"type": "BLOCK_IP", "blocked_ip": "192.168.1.99"},


        "status": "Activo",


    },


    "108": {


        "ip": "192.168.1.80",


        "device_name": "Impresora Oficina",


        "policy": {"type": "ALLOW_ALL"},


        "status": "Inactivo",


    },


    "109": {


        "ip": "192.168.1.90",


        "device_name": "Servidor de Archivos",


        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.95"},


        "status": "Activo",


    },


    "110": {


        "ip": "192.168.1.100",


        "device_name": "Switch Piso 2",


        "policy": {"type": "BLOCK_IP", "blocked_ip": "192.168.1.100"},


        "status": "Activo",


    },


}


@app.route("/json/<mac>")
def json_data(mac):
    if mac not in datos_json:
        return jsonify({"error": "Dispositivo no encontrado"}), 404


    print(datos_json[mac]["Name"])
    print(datos_json[mac]["Protocolos"])
    print(datos_json[mac]["status"])
    print(datos_json[mac]["VLANs"])


    return jsonify(datos_json[mac])




if __name__ == "__main__":
    app.run(debug=True)