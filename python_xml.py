import pymysql

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

############### CONFIGURAR ESTO ###################

# Conexión de base de datos.
conexion = "database-1.c5w3nasbxtpp.us-east-1.rds.amazonaws.com"  # aquí pondremos nuestra dirección de la base de datos de Amazon web services
usuario = "admin"  # usuario de la conexión
password = "48066656z"  # contraseña
BBDD = "proyecto"  # base de datos a la cual nos vamos a conectar
db = pymysql.connect(conexion, usuario, password, BBDD)
##################################################

#query_sql = "SELECT p.idpartida,p.condiciones_victoria, p.ganador_partida,p.duracion FROM partida p "
''' 
query_preuva='select * FROM cartas'
query_prueva2='select * FROM jugador'
querys=[query_preuva,query_prueva2]
'''
query1='WITH MyRowSet AS (select idparticipante,carta_inicial,count(carta_inicial) as "usos",ROW_NUMBER() OVER (PARTITION BY idparticipante) AS "primera_carta" from turnos group by idparticipante,carta_inicial) SELECT * FROM MyRowSet WHERE Primera_carta = 1;'
query2='select u.username, MAX(t.apuesta), t.idpartida from usuario u, turnos t where u.idusuario IN (SELECT j.idusuario from jugador j where j.idjugador IN (SELECT p.id_jugador FROM participante p where p.id_participante IN (SELECT t.idparticipante from turnos t))) group by idpartida;'
#query13='select count(t.carta_inicial) as "Nº carta inicial", sum((select valor from cartas where idcartas = t.carta_inicial)) as "Valor carta", p.idpartida from turnos inner join partida p on p.idpartida = t.idpartida group by idpartida;'

querys=[query1,query2]

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

with open('Resultadoquery.xml', 'w') as outfile:
    outfile.write('<?xml version="1.0" ?>\n')
    for i in querys:
        query_to_xml(i)
outfile.close()


while True:
    n = input_int('Que informe quieres ver?\n1- \n2- ')
    cursor = db.cursor()
    cursor.execute(querys[n-1])
    rows = cursor.fetchall()
    for row in rows:
        for index in range(len(row)):
            print('\t{}: {}\n'.format(cursor.description[index][0], row[index]))
        print('-'*40)
    s = input('Quieres ver otra(SI/NO)? ').upper()
    if s == 'NO':
        break
    elif s != 'SI':
        print('Input no reconocido, interpretado como SI')
db.close()
