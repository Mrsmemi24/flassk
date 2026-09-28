from pickle import APPEND
from turtle import color


nums = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez']
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white']


#ACTIVIDAD  INVIERTE LA LISTA DE NUMS PARA PODER VER LOS ELEMENTOS DE LA LISTA ['DIEZ','ROJO']
#AL FINAL CREAR UNA NUEVA LISTA AMBOS ELEMENTOS E IMPRIMIR LA NUEVA LISTA

nums.reverse()
nuevalista = []


for num in nums:
    output = f"{num}, {colors[nums.index(num)]}"
    nuevalista.append(output)

for cola in nuevalista:
    print(cola)


'''print (num [0], colors [0])'''

#colors.append('orange')
#lleva a la lista el lo que pongas en los parentesis

#colors.extend(['violeta','amarillo'])
#los agrega hasta al final de la lista

#colors.insert(2,'violetaaa')
#agrega en en la casilla lo que agregas

#colors.insert(2,'violetaaa')
#colors.clear()
#colors.clear elima todo, sin que puedas elegir que eliminar
#colors.append('violetaa')
#agrega solamente la palabra que este, o el numero

#colors.sort(reverse=False)
#cuando esta en true, los ordena de mayor a menor
# caundo esta en false, los ordena por orden alfabetico, de menor a mayor

#colors_1 = colors.copy()
#colors_1 = colors.copy() hace una copia de la lista, y la guarda en otra variable, para que no se pierda la lista original


