import random as r
def accion_bot(putnos_carta):
    limite=r.randrange(4,7)
    if putnos_carta>=limite:
        accion='plantado'
    else:
        accion='jugando'
    return accion

def puede_apostar(lista_de_cartas,puntuacion_cartas):
    cantidad_no_moricion=0
    cantidad_si_moricion=0
    for i in lista_de_cartas:
        if puntuacion_cartas+i[2]>7.5:
            cantidad_si_moricion+=1
        else:
            cantidad_no_moricion+=1
    if cantidad_si_moricion>cantidad_no_moricion:
        return 'no'
    else:
        return 'si'

def apuesta_bot(puntos_restantes_bot):
    rng=r.randint(1,11)
    if rng==1:
        apuesta=puntos_restantes_bot
    elif rng>1 and rng<4:
        apuesta=puntos_restantes_bot//2
    elif rng>3 and rng<7:
        apuesta=puntos_restantes_bot//3
    else:
        apuesta=(puntos_restantes_bot//5)
    print('Apuesta: ', apuesta)
    return apuesta

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
quitar=((8,'oros',8),(8,'copas',8),(8,'espadas',8),(8,'bastos',8),(9,'oros',9),(9,'copas',9),(9,'espadas',9),(9,'bastos',9))
for i in quitar:
    cartas.remove(i)
    cartas_backup.remove(i)
# Hacer lista de jugador max 8
bots=input('Desea jugar con bots? (Si/No): ').upper()
if bots=='NO':
    jugadores=[]
    while True:
        numj=int(input('nombre de jugadors(max8): '))
        if numj>8 or numj<0:
            print('input invalid')
        else:
            break
    for i in range(numj):
        Nombre=input("Escriu el nom d'un jugador: ")
        if Nombre.isalnum()==True and Nombre[0].isalpha()==True:
            jugadores.append(Nombre)
        elif Nombre.isalnum()==False:
            print("El nom només pot ser de lletras i números i no pot contenir espais.")
        elif Nombre[0].isalpha()==False:
            print("El primer caràcter del nom ha de ser una lletra.")
elif bots=='SI':
    jugadores=[]
    while True:
        numj=int(input('Cuantos jugadores humanos(max7): '))
        if numj>8 or numj<0:
            print('input invalid')
        else:
            break
    for i in range(numj):
        Nombre=input("Escriu el nom d'un jugador: ")
        if Nombre.isalnum()==True and Nombre[0].isalpha()==True:
            jugadores.append(Nombre)
        elif Nombre.isalnum()==False:
            print("El nom només pot ser de lletras i números i no pot contenir espais.")
        elif Nombre[0].isalpha()==False:
            print("El primer caràcter del nom ha de ser una lletra.")
    numbMAX=8-numj
    numb=int(input('Cuantos bots(max{}): '.format(numbMAX)))
    for i in range(numb):
        jugadores.append('bot{}'.format(i))
# Escoger carta aleatoria por jugador para orden prioridad, Bucle nueva mano 0
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
jugador={}
for i in jugadores:
    jugador[i]=['1ra_carta','estado mano actual','estado partida','prioridad','valor cartas',0,20,'contador mano',]
#Bucle mano por jugador(1)
cont=1
contmano=0
contmano+=1
for i in jugador.keys():
    if cont!=len(jugador.keys()):
        jugador[i][3]=cont
    else:
        jugador[i][3]=0
    if jugador[i][3]==0:
        print('le toca a {}, es la banca'.format(i))
    else:
        print('le toca a {}'.format(i))
    carta_r=r.choice(cartas)
    cartas.remove(carta_r)
    print(carta_r)
    jugador[i][0]=carta_r
    jugador[i][4]=carta_r[2]
    jugador[i][7]=contmano
    if jugador[i][6]>0:
        jugador[i][2]='jugando'
        jugador[i][1]='jugando'
    else:
        jugador[i][2]='eliminado'
        jugador[i][1]='eliminado'
    if i[:3]=='bot' and jugador[i][1]!='eliminado' and jugador[i][3]!=0:
        if puede_apostar(cartas,jugador[i][4]):
            jugador[i][5]=apuesta_bot(jugador[i][6])
            while True:
                jugador[i][1]=accion_bot(jugador[i][4])
                if jugador[i][1]=='jugando':
                    carta_r = r.choice(cartas)
                    cartas.remove(carta_r)
                    print(carta_r)
                    jugador[i][4] += carta_r[2]
                    print('puntos: ', jugador[i][4])
                    if jugador[i][4] > 7.5:
                        jugador[i][1] = 'eliminado'
                        print('te has pasado de 7 y medio')
                        break
                if jugador[i][1]=='plantado':
                    break

        else:
            jugador[i][5]=apuesta_bot(jugador[i][6])
            jugador[i][1]='plantado'
    elif puede_apostar(cartas,jugador[i][4]) and jugador[i][1]!='eliminado' and jugador[i][3]!=0:
            min=jugador[i][6]//5
            while True:
                jugador[i][5]=int(input('apuesta, min {}: '.format(min)))
                if not isinstance(jugador[i][5],int):
                    print('Solo se acepta int como apuesta')
                elif jugador[i][5]<min:
                    print('No se puede apostar menos que el minimo')
                else:
                    break
            while True and jugador[i][1]!='eliminado':
                estado=int(input('Que quieres hacer:\n1)Plantarte\n2)Seguir\n'))
                if estado==1:
                    jugador[i][1]='plantado'
                    break
                elif estado==2:
                    jugador[i][1]='jugando'
                    while True:
                        carta_r = r.choice(cartas)
                        cartas.remove(carta_r)
                        print(carta_r)
                        jugador[i][4]+=carta_r[2]
                        print('puntos: ',jugador[i][4])
                        if jugador[i][4]>7.5:
                            jugador[i][1]='eliminado'
                            print('te has pasado de 7 y medio')
                            break
                        else:
                            break
                else:
                    print('input no valido')
    if jugador[i][3]==0 and i[:3]=='bot':
        while True:
            jugador[i][1] = accion_bot(jugador[i][4])
            if jugador[i][1] == 'jugando':
                carta_r = r.choice(cartas)
                cartas.remove(carta_r)
                print(carta_r)
                jugador[i][4] += carta_r[2]
                print('puntos: ', jugador[i][4])
                if jugador[i][4] > 7.5:
                    jugador[i][1] = 'eliminado'
                    print('te has pasado de 7 y medio')
                    break
            if jugador[i][1] == 'plantado':
                break
    elif jugador[i][3]==0 and i[:3]!='bot':
        while True and jugador[i][1]:
            estado = int(input('Que quieres hacer:\n1)Plantarte\n2)Seguir\n'))
            if estado == 1:
                jugador[i][1] = 'plantado'
                break
            elif estado == 2:
                jugador[i][1] = 'jugando'
                while True:
                    carta_r = r.choice(cartas)
                    cartas.remove(carta_r)
                    print(carta_r)
                    jugador[i][4] += carta_r[2]
                    print('puntos: ', jugador[i][4])
                    if jugador[i][4] > 7.5:
                        jugador[i][1] = 'eliminado'
                        print('te has pasado de 7 y medio')
                        break
                    else:
                        break
                if jugador[i][1]=='eliminado':
                    break
            else:
                print('input no valido')
    jugador[i][6]-=jugador[i][5]
    cont+=1
print(jugador)
#ver quien gana las apuestas, nuevas prioridades y banca, transformar bucles a funciones, que pasa si la banca entra en bancarota?, que los usuarios no se llamen bots


# Bucle mano por jugador 1
# Sub Bucle mano por jugador 2
