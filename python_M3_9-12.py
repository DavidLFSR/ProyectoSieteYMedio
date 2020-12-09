import random as r
def accion_bot(putnos_carta):
    limite=r.randrange(4,7)
    if putnos_carta>=limite:
        accion='plantado'
        print('\tel bot se planta')
    else:
        accion='jugando'
        print('\tel bot roba otra carta')
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

def apuesta_bot(puntos_restantes_bot,limite):
    apostado=False
    if limite[1]>puntos_restantes_bot:
        max=int(puntos_restantes_bot)
    else:
        max=limite[1]
    if limite[0]>puntos_restantes_bot:
        apuesta=puntos_restantes_bot
        apostado=True
    elif puntos_restantes_bot*1/5>limite[0]:
        min=puntos_restantes_bot//5
    else:
        min=limite[0]
    if not apostado:
        apuesta=r.randint(min,max)
    print('\tApuesta: ', apuesta)
    return apuesta

# Lista de tuplas cartas
# mazo =[( valor real , prioridad , valor en el juego )]
limit=[2,5],[3,7],[4,9],[6,12] #[minimo,maximo]
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
############DEFINICION_USUARIOS##################################3
def usuarios():
    global jugadores
    bots=input('Desea jugar con bots? (Si/No): ').upper()
    if bots=='NO':
        jugadores=[]
        while True:
            while True:
                numj=int(input('nombre de jugadors(max8): '))
                if numj!=1:
                    break
                else:
                    print('no puedes jugar solo')
            if numj>8 or numj<0:
                print('input invalid')
            else:
                break
        for i in range(numj):
            while True:
                Nombre=input("Escriu el nom d'un jugador: ")
                if Nombre[:3]=='bot':
                    print('el jugador no se puede llamar bot al inicio de su nombre')
                elif Nombre.isalnum()==True and Nombre[0].isalpha()==True:
                    jugadores.append(Nombre)
                    break
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
            while True:
                Nombre=input("Escriu el nom d'un jugador: ")
                if Nombre[:3]=='bot':
                    print('el jugador no se puede llamar bot al inicio de su nombre')
                elif Nombre.isalnum()==True and Nombre[0].isalpha()==True:
                    jugadores.append(Nombre)
                    break
                elif Nombre.isalnum()==False:
                    print("El nom només pot ser de lletras i números i no pot contenir espais.")
                elif Nombre[0].isalpha()==False:
                    print("El primer caràcter del nom ha de ser una lletra.")
        numbMAX=8-numj
        numb=int(input('Cuantos bots(max{}): '.format(numbMAX)))
        for i in range(numb):
            jugadores.append('bot{}'.format(i))
###########################ORDEN_JUGADORES(bucle 0)###################################
# Escoger carta aleatoria por jugador para orden prioridad, Bucle nueva mano 0
def orden_jugadores():
    global jugadores
    global cartas
    for i in range(len(jugadores)):     #bucle para dar 1 carta a cada jugador        #para que no se repitan las cartas
        carta=r.choice(cartas)
        cartas.remove(carta)
        print('{} ha sacado un {} de {}'.format(jugadores[i],carta[0],carta[1]))
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
    input('---pulsa enter para continuar---')

def reset_mazo(mazo,backup_mazo):
    mazo=[]
    for i in backup_mazo:  #reinicio el mazo
        mazo.append(i)
#####################INICIO_DICCIONARIO_JUG##################################
# Diccionario con tuplas de cada jugador (La clave es el nombre del jugador y los valores son una lista de elementos

#Bucle mano por jugador(1)
#######################BUCLE_MANO_JUGADOR(1)############################
def mano():
    global cont
    global contmano
    global jugadores
    global jugador
    global limit
    contmano+=1
    for i in jugador.keys():
        if contmano<30*1/4:
            limit_mano=limit[0]
        elif contmano<30*1/2:
            limit_mano=limit[1]
        elif contmano<30*3/4:
            limit_mano=limit[2]
        else:
            limit_mano=limit[3]
        print('rango de apuestas para esta ronda: {} a {}'.format(limit_mano[0],limit_mano[1]))
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
        print('\tsaca un {} de {}, vale {}'.format(carta_r[0],carta_r[1],carta_r[2]))
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
                jugador[i][5]=apuesta_bot(jugador[i][6],limit_mano)
                while True:
                    jugador[i][1]=accion_bot(jugador[i][4])
                    if jugador[i][1]=='jugando':
                        carta_r = r.choice(cartas)
                        cartas.remove(carta_r)
                        print('\tsaca un {} de {}, vale {}'.format(carta_r[0],carta_r[1],carta_r[2]))
                        jugador[i][4] += carta_r[2]
                        print('\tpuntos: ', jugador[i][4])
                        if jugador[i][4] > 7.5:
                            jugador[i][1] = 'eliminado'
                            print('\tte has pasado de 7 y medio')
                            break
                    if jugador[i][1]=='plantado':
                        break

            else:
                jugador[i][5]=apuesta_bot(jugador[i][6])
                jugador[i][1]='plantado'
        elif puede_apostar(cartas,jugador[i][4]) and jugador[i][1]!='eliminado' and jugador[i][3]!=0:
            min=jugador[i][6]//5
            if limit_mano[1] > jugador[i][6]:
                max = jugador[i][6]
            else:
                max = limit_mano[1]
            if limit_mano[0] > jugador[i][6]:
                apuesta = jugador[i][6]
            elif jugador[i][6] * 1 // 5 > limit_mano[0]:
                min = jugador[i][6] * 1 // 5
            else:
                min = limit_mano[0]
            while True:
                jugador[i][5]=int(input('\tapuesta, min {} max {}, tienes {} puntos: '.format(min,max,jugador[i][6])))
                if not isinstance(jugador[i][5],int):
                    print('\tSolo se acepta int como apuesta')
                elif jugador[i][5]<min:
                    print('\tNo se puede apostar menos que el minimo')
                elif jugador[i][5]>max:
                    print('\tNo se puede apostar mas del maximo')
                elif jugador[i][5]>jugador[i][6]:
                    print('\tNo se puede apostar mas de lo que tienes')
                else:
                    break
            while True and jugador[i][1]!='eliminado':
                estado=int(input('\tQue quieres hacer:\n\t\t1)Plantarte\n\t\t2)Seguir\n'))
                if estado==1:
                    jugador[i][1]='plantado'
                    break
                elif estado==2:
                    jugador[i][1]='jugando'
                    while True:
                        carta_r = r.choice(cartas)
                        cartas.remove(carta_r)
                        print('\tsaca un {} de {}, vale {}'.format(carta_r[0],carta_r[1],carta_r[2]))
                        jugador[i][4]+=carta_r[2]
                        print('\tpuntos: ',jugador[i][4])
                        if jugador[i][4]>7.5:
                            jugador[i][1]='eliminado'
                            print('\tte has pasado de 7 y medio')
                            break
                        else:
                            break
                else:
                    print('\tinput no valido')
        if jugador[i][3]==0 and i[:3]=='bot':
            while True:
                jugador[i][1] = accion_bot(jugador[i][4])
                if jugador[i][1] == 'jugando':
                    carta_r = r.choice(cartas)
                    cartas.remove(carta_r)
                    print('\tsaca un {} de {}, vale {}'.format(carta_r[0],carta_r[1],carta_r[2]))
                    jugador[i][4] += carta_r[2]
                    print('\tpuntos: ', jugador[i][4])
                    if jugador[i][4] > 7.5:
                        jugador[i][1] = 'eliminado'
                        print('\tte has pasado de 7 y medio')
                        break
                if jugador[i][1] == 'plantado':
                    break
        elif jugador[i][3]==0 and i[:3]!='bot':
            while True and jugador[i][1]:
                estado = int(input('\tQue quieres hacer:\n\t\t1)Plantarte\n\t\t2)Seguir\n'))
                if estado == 1:
                    jugador[i][1] = 'plantado'
                    break
                elif estado == 2:
                    jugador[i][1] = 'jugando'
                    while True:
                        carta_r = r.choice(cartas)
                        cartas.remove(carta_r)
                        print('\tsaca un {} de {}, vale {}'.format(carta_r[0],carta_r[1],carta_r[2]))
                        jugador[i][4] += carta_r[2]
                        print('\tpuntos: ', jugador[i][4])
                        if jugador[i][4] > 7.5:
                            jugador[i][1] = 'eliminado'
                            print('\tte has pasado de 7 y medio')
                            break
                        else:
                            break
                    if jugador[i][1]=='eliminado':
                        break
                else:
                    print('\tinput no valido')
        input('---pulsa enter para continuar---')
        jugador[i][6]-=jugador[i][5]
        cont+=1
##########################COMPARACION_PUNTUACIONES########################################
#ver quien gana las apuestas
def apuestas():
    global jugador
    global jugadores
    global partida
    puntos_B=jugador[jugadores[-1]][4]
    if puntos_B>7.5:
        puntos_B=0
    sieteymedio=[]
    conseguido=False
    for i in jugadores[:-1]:
        puntos_J=jugador[i][4]
        if puntos_J>7.5:
            puntos_J=0
        if puntos_J>puntos_B and puntos_J==7.5:
            if jugador[jugadores[-1]][6]-jugador[i][5]*2<0:
                jugador[i][6]+=jugador[jugadores[-1]][6]
                jugador[jugadores[-1]][6]=0
            else:
                jugador[i][6]+=jugador[i][5]*3
                jugador[jugadores[-1]][6]-=jugador[i][5]*2
            print('{} gana {}'.format(i,jugador[i][5]*3))
            jugador[i][5] = 0
            sieteymedio.append([i,jugador[i][3]])
            conseguido=True
        elif puntos_J>puntos_B:
            if jugador[jugadores[-1]][6]-jugador[i][5]<0:
                jugador[i][6]+=jugador[jugadores[-1]][6]
                jugador[jugadores[-1]][6]=0
            else:
                jugador[i][6]+=jugador[i][5]*2
                jugador[jugadores[-1]][6]-=jugador[i][5]
            print('{} gana {}'.format(i,jugador[i][5] * 2))         #Se puede poner que printe la cantidad que pierde la banca al final del turno
            jugador[i][5] = 0
        else:
            jugador[jugadores[-1]][6]+=jugador[i][5]
            print('{}(banca) gana {}'.format(jugadores[-1],jugador[i][5]))
            jugador[i][5] = 0
    input('---pulsa enter para continuar---')
    #nuevas prioridades y banca,
    if conseguido:
        if len(sieteymedio)!=1:
            min=9 #como hay maximo 8 jugadores no va a haber una prioridad mayor a 9
            for i in range(sieteymedio):
                if sieteymedio[i][1]<min:
                    min=sieteymedio[i][1]
                    minpos=i
            sieteymedio=sieteymedio[minpos][0]
        if len(sieteymedio)==1:
            sieteymedio=sieteymedio[0][0]
        jugadores.remove(sieteymedio)
        jugadores.append(sieteymedio)
    for i in jugador:
        if jugador[i][6]<=0:
            jugador[i][2]='eliminado'
    eliminados=0
    for i in jugador:
        if jugador[i][2]=='eliminado':
            eliminados+=1
    if eliminados==len(jugadores)-1:
        partida=False
####################################################################
# transformar bucles a funciones,

#JUEGO#
partida=True
usuarios()
orden_jugadores()
reset_mazo(cartas,cartas_backup)
jugador={}
for i in jugadores:
    jugador[i]=['1ra_carta','estado mano actual','estado partida','prioridad','valor cartas',0,20,'contador mano',]
cont=1
contmano=0
while contmano<=30 and partida:
    mano()
    apuestas()

#Resetearm cartas al acabar turno, enseñar info de jugs a medida que pasan turnos