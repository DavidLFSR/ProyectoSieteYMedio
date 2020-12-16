import random as r
import xml.etree.ElementTree as ET
import pymysql

############### CONFIGURAR ESTO ###################

# Conexión de base de datos.
conexion = "database-1.c5w3nasbxtpp.us-east-1.rds.amazonaws.com"  # aquí pondremos nuestra dirección de la base de datos de Amazon web services
usuario = "admin"  # usuario de la conexión
password = "48066656z"  # contraseña
BBDD = "proyecto"  # base de datos a la cual nos vamos a conectar
db = pymysql.connect(conexion, usuario, password, BBDD)
##################################################
#query_preuva='select * FROM cartas'
#query_prueva2='select * FROM jugador'
#querys=[query_preuva,query_prueva2]

query1='WITH MyRowSet AS (select idparticipante,carta_inicial,count(carta_inicial) as "usos",ROW_NUMBER() OVER (PARTITION BY idparticipante) AS "primera_carta" from turnos group by idparticipante,carta_inicial) SELECT * FROM MyRowSet WHERE Primera_carta = 1;'
query2='select nombre,max(apuesta),idpartida from (select case when username is not null then usuario.username else descripcion end as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username) tabla where (apuesta,idpartida) in (select max(turnos.apuesta),partida.idpartida as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by max(turnos.apuesta) desc) group by idpartida;'
query3='select nombre,min(apuesta),idpartida from (select case when username is not null then usuario.username else descripcion end as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username) tabla where (apuesta,idpartida) in (select min(turnos.apuesta),partida.idpartida as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by min(turnos.apuesta) desc) group by idpartida;'
query11='select avg(t.apuesta) as "Media", p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida group by idpartida;'
query13='select count(carta_inicial) AS numero_de_cartas, sum(valor) AS valor_total, idpartida AS partida from turnos, cartas where carta_inicial=idcartas group by idpartida;'
querys=[query1,query2,query3,query11,query13]

def query_to_xml(query_sql):
    outfile.write('<query>\n')
    db = pymysql.connect(conexion, usuario, password, BBDD)
    cursor = db.cursor()
    cursor.execute(query_sql)
    rows = cursor.fetchall()
    for row in rows:
        outfile.write('  <row>\n')
        for index in range(len(row)):

            outfile.write('       <{}>{}</{}>\n'.format(cursor.description[index][0],row[index],cursor.description[index][0]))
        outfile.write('\n  </row>\n')
    outfile.write('</query>\n')

limit=[2,5],[3,7],[4,9],[6,12] #[minimo,maximo]
palos_prio={'Oros':1, 'Copas':2, 'Espadas':3, 'Bastos':4}

tree=ET.parse('Cartas.xml') # mazo =[( valor real , prioridad , valor en el juego )]
root= tree.getroot()        # cargo el mazo de xml
cartas=[]
cartas_backup=[]
for carta in root:
    cont=0
    for sub in carta:
        if cont == 0:
            id=sub.text
        elif cont == 1:
            valor=int(sub.text)
        elif cont == 2:
            palo=sub.text
        elif cont == 3:
            valor_j=float(sub.text)
        elif cont == 4:
            activa=sub.text
        cont+=1
    if activa=='SI':
        tupla=(valor,palo,valor_j)
        cartas.append(tupla)
        cartas_backup.append(tupla)
tree=ET.parse('Basic_Config_Game.xml')  #cargo las reglas del xml
root= tree.getroot()
cont=0
for config in root:
    if cont==0:
        min_j=int(config.text)
    elif cont==1:
        max_j=int(config.text)
    elif cont==2:
        max_r=int(config.text)
    elif cont==3:
        init_points=int(config.text)
    elif cont==4:
        auto_mode=bool(config.text)
    cont+=1

def input_int(texto):
    while True:
        entrada=input(texto)
        try:
            entrada=int(entrada)
        except:
            print('escribe un int')
        else:
            break
    return entrada

def pausa():
    input('----pulsa enter para continuar----')


def reset_mazo():
    global cartas
    global cartas_backup
    cartas=[]
    for i in cartas_backup:  #reinicio el mazo
        cartas.append(i)

#FUNCIONES DEL BOT
def accion_bot(lista_cartas,putnos_cartas):
    cantidad_no_muerte = 0
    cantidad_si_muerte = 0
    for i in lista_cartas:
        if putnos_cartas + i[2] > 7.5:
            cantidad_si_muerte += 1
        else:
            cantidad_no_muerte += 1
    chance=(cantidad_no_muerte/(cantidad_si_muerte+cantidad_no_muerte))*100
    if chance>65:
        return 'jugando'
    elif chance>=50:
        rng=r.randint(1,100)
        if rng<=chance:
            return 'jugando'
        else:
            return 'plantado'
    else:
        rng=r.randint(1,100)
        if rng<=chance/3:
            return 'jugando'
        else:
            return 'plantado'

def accion_bot_banca(punt_max_jugadores,puntuacion_cartas):
    global maxima_puntuacion
    if puntuacion_cartas<maxima_puntuacion:
        return 'jugando'
    else:
        return 'plantado'

def maxima_punt(puntos_jugador):
    global maxima_puntuacion
    if puntos_jugador<=7.5:
        if puntos_jugador>maxima_puntuacion:
            maxima_puntuacion=puntos_jugador

def apuesta_bot(puntos_restantes_bot,limite):
    apostado=False
    if limite[1]>puntos_restantes_bot:
        max=int(puntos_restantes_bot)
    else:
        max=limite[1]
    if limite[0]>puntos_restantes_bot:
        apuesta=puntos_restantes_bot
        apostado=True
    elif puntos_restantes_bot//5>limite[0]:
        min=int(puntos_restantes_bot*1/5)
    else:
        min=limite[0]
    if puntos_restantes_bot//5>limite[1]:
        apuesta=limite[1]
        apostado=True
    if not apostado:
        apuesta=r.randint(min,max)
    print('\tApuesta: ', apuesta)
    return apuesta

#FUNCION PARA DEFINIR LOS USUARIOS
def usuarios():
    global jugadores
    while True:
        bots=input('Desea jugar con bots? (Si/No): ').upper()
        if bots=='NO':
            jugadores=[]
            while True:
                numj=input_int('nombre de jugadors(max{}): '.format(max_j))
                if numj<min_j:
                    print('no pueden jugar menos de {}'.format(min_j))
                elif numj>max_j:
                    print('no pueden jugar mas que {}'.format(max_j))
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
            break
        elif bots=='SI':
            jugadores=[]
            if auto_mode:
                min_j_h = 0
            else:
                min_j_h = 1
            while True:
                numj=input_int('Cuantos jugadores humanos(max{}): '.format((max_j-1)))
                if numj>max_j or numj < min_j_h:
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
            numbMAX=max_j-numj
            if numj==0:
                numbMIN=2
            else:
                numbMIN=1
            while True:
                numb=input_int('Cuantos bots(max{}): '.format(numbMAX))
                if numb<numbMIN:
                    print('el numero de bots no puede ser menos que {}'.format(numbMIN))
                elif numb>numbMAX:
                    print('el numero de bots no puede ser mas que {}'.format(numbMAX))
                else:
                    break
            for i in range(numb):
                jugadores.append('bot{}'.format(i))
            break
        else:
            print('input  no valido')

#FUNCION PARA ORDENAR LOS JUGADORES
def orden_jugadores():      # Escoger carta aleatoria por jugador para orden prioridad
    global jugadores
    global cartas
    for i in range(len(jugadores)):     #Dar 1 carta a cada jugador
        carta=r.choice(cartas)
        print('{} saca {} de {}'.format(jugadores[i],carta[0],carta[1]))
        cartas.remove(carta)            #Quito la carta para que no se repita
        jugadores[i]=jugadores[i],carta
    for i in range(len(jugadores)-1):   #ordeno x burbuja
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
    reset_mazo()    #reset del mazo

#INICIO DE MANO
def mano():
    global contmano
    global jugadores
    global jugador
    global limit
    cont=1
    contmano+=1
    print('{:>20}'.format('mano'),'{}'.format(contmano))
    if contmano < 30 * 1 / 4:   #segun la mano en la que se este el limite de apuestas sera uno o otro
        limit_mano = limit[0]
    elif contmano < 30 * 1 / 2:
        limit_mano = limit[1]
    elif contmano < 30 * 3 / 4:
        limit_mano = limit[2]
    else:
        limit_mano = limit[3]
    print('rango de apuestas para esta ronda: {} a {}'.format(limit_mano[0], limit_mano[1]))
    for i in jugadores:                     #segun su posicion en la lista ordenada le doy la prioridad que le pertoca
        if cont!=len(jugadores):
            jugador[i][3]=cont
        else:
            jugador[i][3]=0
        if jugador[i][2]=='eliminado':
            print('\t{} ELIMINADO'.format(i))
            jugadores.remove(i)
        else:
            if jugador[i][3]==0:
                print('le toca a {}, es la banca'.format(i))
                eliminados = 0
                for j in jugadores[:-1]:
                    if jugador[j][1] == 'eliminado':
                        eliminados += 1
                if eliminados == len(jugadores) - 1:
                    print('no hace falta que la banca robe')
                    jugador[i][4]=0
                else:
                    print('tienes {} puntos restantes'.format(jugador[i][6]))
                    carta_r = r.choice(cartas)  # roba carta
                    cartas.remove(carta_r)
                    print('\tha robado {} de {}'.format(carta_r[0], carta_r[1]))
                    jugador[i][0] = carta_r
                    jugador[i][4] = carta_r[2]  # los puntos de la cartaa
                    print('\tpuntos: ', jugador[i][4])
                    jugador[i][7] = contmano
                    jugador[i][2] = 'jugando'
                    jugador[i][1] = 'jugando'
                    if jugador[i][3] == 0 and i[:3] == 'bot':
                        while True:
                            jugador[i][1] = accion_bot_banca(maxima_puntuacion, jugador[i][4])
                            if jugador[i][1] == 'jugando':
                                carta_r = r.choice(cartas)
                                cartas.remove(carta_r)
                                print('\tha robado {} de {}'.format(carta_r[0], carta_r[1]))
                                jugador[i][4] += carta_r[2]
                                print('\tpuntos: ', jugador[i][4])
                                if jugador[i][4] > 7.5:
                                    jugador[i][1] = 'eliminado'
                                    print('\tte has pasado de 7 y medio')
                                    break
                            if jugador[i][1] == 'plantado':
                                break
                    elif jugador[i][3] == 0 and i[:3] != 'bot':
                        while True and jugador[i][1]!='eliminado':
                            estado = input('\tQue quieres hacer:\n\t\t1)Plantarte\n\t\t2)Seguir ')
                            if estado == '1':
                                jugador[i][1] = 'plantado'
                                break
                            elif estado == '2':
                                jugador[i][1] = 'jugando'
                                while True:
                                    carta_r = r.choice(cartas)
                                    cartas.remove(carta_r)
                                    print('\tha robado {} de {}'.format(carta_r[0], carta_r[1]))
                                    jugador[i][4] += carta_r[2]
                                    print('\tpuntos: ', jugador[i][4])
                                    if jugador[i][4] > 7.5:
                                        jugador[i][1] = 'eliminado'
                                        print('\tte has pasado de 7 y medio')
                                        break
                                    else:
                                        break
                                if jugador[i][1] == 'eliminado':
                                    break
                            else:
                                print('\tinput no valido')

            else:
                print('le toca a {}'.format(i))
                print('tienes {} puntos restantes'.format(jugador[i][6]))
                carta_r=r.choice(cartas)    #roba carta
                cartas.remove(carta_r)
                print('\tha robado {} de {}'.format(carta_r[0],carta_r[1]))
                jugador[i][0]=carta_r
                jugador[i][4]=carta_r[2]    #los puntos de la cartaa
                print('\tpuntos: ', jugador[i][4])
                jugador[i][7]=contmano
                jugador[i][2]='jugando'
                jugador[i][1]='jugando'
                if i[:3]=='bot':
                    jugador[i][5]=apuesta_bot(jugador[i][6],limit_mano)
                    while True:
                        jugador[i][1]=accion_bot(cartas,jugador[i][4])
                        if jugador[i][1]=='jugando':
                            carta_r = r.choice(cartas)
                            cartas.remove(carta_r)
                            print('\tha robado {} de {}'.format(carta_r[0],carta_r[1]))
                            jugador[i][4] += carta_r[2]
                            print('\tpuntos: ', jugador[i][4])
                            if jugador[i][4] > 7.5:
                                jugador[i][1] = 'eliminado'
                                print('\tte has pasado de 7 y medio')
                                break
                        if jugador[i][1]=='plantado':
                            break
                else:
                    apostado=False
                    min=jugador[i][6]//5
                    if limit_mano[0] > jugador[i][6]:
                        apuesta = jugador[i][6]
                        jugador[i][5]=apuesta
                        print('\tapuesta: {}'.format(apuesta))
                        apostado=True
                    elif jugador[i][6] * 1 / 5 > limit_mano[0]:
                        min = jugador[i][6] // 5
                    else:
                        min = limit_mano[0]
                    while True and not apostado:
                        jugador[i][5]=input_int('\tapuesta, min {}: '.format(min,max))
                        if jugador[i][5]<min:
                            print('\tNo se puede apostar menos que el minimo')
                        elif jugador[i][6]<jugador[i][5]:
                            print('\tNo puedes apostar más de lo que tienes')
                        else:
                            break
                    while True and jugador[i][1]!='eliminado':
                        estado=input('\tQue quieres hacer:\n\t\t1)Plantarte\n\t\t2)Seguir ')
                        if estado=='1':
                            jugador[i][1]='plantado'
                            break
                        elif estado=='2':
                            jugador[i][1]='jugando'
                            carta_r = r.choice(cartas)
                            cartas.remove(carta_r)
                            print('\tha robado {} de {}'.format(carta_r[0],carta_r[1]))
                            jugador[i][4]+=carta_r[2]
                            print('\tpuntos: ',jugador[i][4])
                            if jugador[i][4]>7.5:
                                jugador[i][1]='eliminado'
                                print('\tte has pasado de 7 y medio')
                                break
                        else:
                            print('\tinput no valido')
        jugador[i][6]-=jugador[i][5]
        cont+=1
        maxima_punt(jugador[i][4])
        pausa()

#VER QUIEN GANA LAS APUESTAS
def apuestas():
    global jugador
    global jugadores
    global partida
    global actu_prio
    global ganador
    actu_prio=False
    puntos_B=jugador[jugadores[-1]][4]
    if puntos_B>7.5:
        puntos_B=0
    sieteymedio=[]
    conseguido=False
    for i in jugadores[:-1]:
        if jugador[i][2]!='eliminado':
            puntos_J=jugador[i][4]
            if puntos_J>7.5:
                puntos_J=0
            if puntos_J>puntos_B and puntos_J==7.5:
                if jugador[jugadores[-1]][6]<jugador[i][5]*2:
                    ganancia=jugador[jugadores[-1]][6]+jugador[i][5]
                    jugador[i][6]+=ganancia
                    jugador[jugadores[-1]][6]=0
                else:
                    ganancia=jugador[i][5]*3
                    jugador[i][6]+=ganancia
                    jugador[jugadores[-1]][6]-=jugador[i][5]*2
                print('{} gana {}'.format(i,ganancia))
                jugador[i][5] = 0
                sieteymedio.append([i,jugador[i][3]])
                conseguido=True
            elif puntos_J>puntos_B:
                if jugador[jugadores[-1]][6]-jugador[i][5]<0:
                    ganancia=jugador[jugadores[-1]][6]+jugador[i][5]
                    jugador[i][6]+=ganancia
                    jugador[jugadores[-1]][6]=0
                else:
                    ganancia=jugador[i][5]*2
                    jugador[i][6]+=ganancia
                    jugador[jugadores[-1]][6]-=jugador[i][5]
                print('{} gana {}'.format(i,ganancia))
                jugador[i][5] = 0
            else:
                jugador[jugadores[-1]][6]+=jugador[i][5]
                print('{}(banca) gana {}'.format(jugadores[-1],jugador[i][5]))
                jugador[i][5] = 0
    #nuevas prioridades y banca,
    if conseguido:
        if len(sieteymedio)!=1:
            min=9 #como hay maximo 8 jugadores no va a haber una prioridad mayor a 9
            for j in range(len(sieteymedio)):
                if sieteymedio[j][1]<min:
                    min=sieteymedio[j][1]
                    minpos=j
            sieteymedio=sieteymedio[minpos][0]
        if len(sieteymedio)==1:
            sieteymedio=sieteymedio[0][0]
        jugadores.remove(sieteymedio)
        jugadores.append(sieteymedio)
        actu_prio=True
    for i in jugador.keys():
        if jugador[i][6]<=0:
            jugador[i][2]='eliminado'
            jugador[i][1]='eliminado'
            if i in jugadores:
                print(i ,' ELIMINADO')
                jugadores.remove(i)
    eliminados=0
    for i in jugador.keys():
        if jugador[i][2]=='eliminado':
            eliminados+=1
        else:
            ganador=i
    if eliminados==len(jugador.keys())-1:
        partida=False

informes=False
while True:
    if not informes:
        que=input('Que quieres hacer?\n1- Jugar\n2- Ver informes\n3- Salir\n')
    if que=='1':
        # JUEGO#
        partida = True
        usuarios()
        orden_jugadores()
        pausa()
        jugador = {}
        for i in jugadores:
            jugador[i] = ['1ra_carta', 'estado mano actual', 'estado partida', 'prioridad', 'valor cartas', 0,
                          init_points, 'contador mano', ]
        contmano = 0
        while contmano < max_r and partida:
            maxima_puntuacion = 0
            mano()
            apuestas()
            reset_mazo()
            pausa()
        if not partida:
            print('HA GANADO {}'.format(ganador))
        else:
            max = 0
            for i in jugador.keys():
                if jugador[i][6] > max:
                    max = jugador[i][6]
                    ganador = i
            print('HA GANADO {} porque se han acabado los turnos'.format(ganador))
        break
    elif que=='2':
        with open('Resultadoquery.xml', 'w') as outfile:
            outfile.write('<?xml version="1.0" ?>\n')
            for i in querys:
                query_to_xml(i)
        outfile.close()

        while True:
            n = input_int('Que informe quieres ver?\n1- \n2- \n3- \n4- \n5- \n')
            cursor = db.cursor()
            cursor.execute(querys[n - 1])
            rows = cursor.fetchall()
            for row in rows:
                for index in range(len(row)):
                    print('\t{}: {}\n'.format(cursor.description[index][0], row[index]))
                print('-' * 40)
            s = input('Quieres ver otra(SI/NO)? ').upper()
            if s == 'NO':
                break
            elif s != 'SI':
                print('Input no reconocido, interpretado como SI')
        db.close()
        while True:
            ahora=input('Quieres jugar al juego(SI/NO)? ').upper()
            if ahora=='SI':
                informes=True
                que='1'
                break
            elif ahora=='NO':
                informes=True
                que='3'
                break
            else:
                print('input no valido')
    elif que=='3':
        break
    else:
        print('input no vàlido')