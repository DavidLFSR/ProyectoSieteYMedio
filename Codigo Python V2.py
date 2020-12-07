import random as r
# Lista de tuplas cartas
# mazo =[( valor real , prioridad , valor en el juego )]
palos_prio={'oros':1, 'copas':2, 'espadas':3, 'bastos':4}
cartas=[(1,'oros',1),(2,'oros',2),(3,'oros',3),(4,'oros',4),(5,'oros',5),(6,'oros',6),(7,'oros',7),(8,'oros',8),(9,'oros',9),(10,'oros',0.5),(11,'oros',0.5),(12,'oros',0.5),
        (1,'copas',1),(2,'copas',2),(3,'copas',3),(4,'copas',4),(5,'copas',5),(6,'copas',6),(7,'copas',7),(8,'copas',8),(9,'copas',9),(10,'copas',0.5),(11,'copas',0.5),(12,'copas',0.5),
        (1,'espadas',1),(2,'espadas',2),(3,'espadas',3),(4,'espadas',4),(5,'espadas',5),(6,'espadas',6),(7,'espadas',7),(8,'espadas',8),(9,'espadas',9),(10,'espadas',0.5),(11,'espadas',0.5),(12,'espadas',0.5),
        (1,'bastos',1),(2,'bastos',2),(3,'bastos',3),(4,'bastos',4),(5,'bastos',5),(6,'bastos',6),(7,'bastos',7),(8,'bastos',8),(9,'bastos',9),(10,'bastos',0.5),(11,'bastos',0.5),(12,'bastos',0.5)]
cartas_backup=[(1,'oros',1),(2,'oros',2),(3,'oros',3),(4,'oros',4),(5,'oros',5),(6,'oros',6),(7,'oros',7),(8,'oros',8),(9,'oros',9),(10,'oros',0.5),(11,'oros',0.5),(12,'oros',0.5),
        (1,'copas',1),(2,'copas',2),(3,'copas',3),(4,'copas',4),(5,'copas',5),(6,'copas',6),(7,'copas',7),(8,'copas',8),(9,'copas',9),(10,'copas',0.5),(11,'copas',0.5),(12,'copas',0.5),
        (1,'espadas',1),(2,'espadas',2),(3,'espadas',3),(4,'espadas',4),(5,'espadas',5),(6,'espadas',6),(7,'espadas',7),(8,'espadas',8),(9,'espadas',9),(10,'espadas',0.5),(11,'espadas',0.5),(12,'espadas',0.5),
        (1,'bastos',1),(2,'bastos',2),(3,'bastos',3),(4,'bastos',4),(5,'bastos',5),(6,'bastos',6),(7,'bastos',7),(8,'bastos',8),(9,'bastos',9),(10,'bastos',0.5),(11,'bastos',0.5),(12,'bastos',0.5)]
# Hacer lista de jugador max 8
bots=input('Desea jugar con bots? (Si/No): ').upper()
if bots=='NO':
    jugadores=[]
    while True:
        numj=int(input('Nombre de jugadores (Máximo 8): '))
        if numj>8 or numj<0:
            print('input invalid')
        else:
            break
    for i in range(numj):
        Nombre=input("Escribe el nombre de un jugador: ")
        if Nombre.isalnum()==True and Nombre[0].isalpha()==True and Nombre.startswith("bot")==False:
            jugadores.append(Nombre)
        elif Nombre.isalnum()==False:
            print("El nombre solo puede contener letras y números y no puede contener espacios.")
        elif Nombre[0].isalpha()==False:
            print("El primer carácter del nombre tiene que ser una letra.")
        elif Nombre.startswith("bot")==True:
            print("El nombre no puede comenzar por bot.")
elif bots=='SI':
    jugadores=[]
    while True:
        numj=int(input('Cuantos jugadores humanos (Máximo 7): '))
        if numj>8 or numj<0:
            print('input invalid')
        else:
            break
    for i in range(numj):
        Nombre = input("Escribe el nombre de un jugador: ")
        if Nombre.isalnum() == True and Nombre[0].isalpha() == True and Nombre.startswith("bot") == False:
            jugadores.append(Nombre)
        elif Nombre.isalnum() == False:
            print("El nombre solo puede contener letras y números y no puede contener espacios.")
        elif Nombre[0].isalpha() == False:
            print("El primer carácter del nombre tiene que ser una letra.")
        elif Nombre.startswith("bot") == True:
            print("El nombre no puede comenzar por bot.")
    numbMAX=8-numj
    numb=int(input('Cuantos bots (Máximo{}): '.format(numbMAX)))

# Escoger carta aleatoria por jugador para orden prioridad
cartas_cojidas=[]
for i in range(len(jugadores)):     #bucle para dar 1 carta a cada jugador
    repe=True
    while repe:                     #para que no se repitan las cartas
        carta=r.choice(cartas)
        if carta not in cartas_cojidas:
            repe=False
    cartas_cojidas.append(carta)
    jugadores[i]=jugadores[i],carta
for i in range(len(jugadores)-1):   #ordeno x burbuha
    for j in range(len(jugadores)-1):
        k=j+1
        if jugadores[j][1][0]>jugadores[k][1][0]:
            aux=jugadores[j]
            jugadores[j]=jugadores[k]
            jugadores[k]=aux    #si el palo coincide gana el que tiene prioridad mas baja
for i in range(1,len(jugadores)):
    if jugadores[i-1][1][0]==jugadores[i][1][0]:
        prio1=palos_prio[jugadores[i-1][1][1]]
        prio2=palos_prio[jugadores[i][1][1]]
        if prio1<prio2:
            aux=jugadores[i]
            jugadores[i]=jugadores[i-1]
            jugadores[i-1]=aux
for i in range(len(jugadores)):         #le quito la carta a los jugadores
    jugadores[i]=jugadores[i][0]
print(jugadores)

# Diccionario con tuplas de cada jugador (La clave es el nombre del jugador y los valores son una lista de elementos
temp=['1ra_carta','estado mano actual','estado partida','prioridad','valor cartas','puntos apostados mano actual','puntos restantes','contador mano']
jugador={}
for i in jugadores:
    jugador[i]=temp
cont=1
for i in jugador.keys():
    carta_r=r.choice(cartas)
    cartas.remove(carta_r)
    jugador[i][0]=carta_r
    jugador[i][1]='jugando'
    jugador[i][2]='jugando'

    if cont!=len(jugador.keys()):
        jugador[i][3]=cont
    else:
        jugador[i][3]=0
    jugador[i][4]=carta_r[2]
    cont+=1
    print(jugador[i])
print(jugador)
# Bucle nueva mano 0
# Bucle mano por jugador 1
# Sub Bucle mano por jugador 2
# Fin Bucle mano por jugador 1
# Fin Sub Bucle mano por jugador 2