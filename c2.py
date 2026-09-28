week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes','Sabado','Domingo' ]
out = []

for day in week:
    if day =='Martes' or day == 'Domingo':
            index = week.index(day)
            out.append(index)

print(out)