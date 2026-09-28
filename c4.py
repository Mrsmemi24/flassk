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

'''''
a= [1,4,6, [7.8,3]]
yaEnUso = a.pop(3)
print(yaEnUso)

contenido = net_config.get("001")
listaA = contenido.get('lista')
num = listaA[2]
print(num)
'''''


net_config ['0002'] = {"Ip": 1}
print (net_config)




'''''
se segmenta para no estar usando .get siempre
'''''

#print (net_config.get("001").get("lista")[2])




#SON RANGOS DE SALTOS PARA NUMEROS.
'''''
i = ()
for i in range (5):
    print (i)
'''
#tAMBIEN SE PUEDE PONER EL NUMERO DE INICIO Y EL NUMERO FINAL
'''''
i = ()
for i in range (5,10):
    print (i)
'''
#O PODER PONER EL NUMERO DE INICIO Y EL NUMERO FINAL Y EL SALTO
'''''
i = ()
for i in range (5,10,2):
    print (i)
'''


