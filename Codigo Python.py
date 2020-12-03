# Lista de tuplas Mazo
mazo=[(1, "oros" ,1),(2, "oros" ,2),(3, "oros" ,3),
      (4, "oros" ,4),(5, "oros" ,5),(6, "oros" ,6),
      (7, "oros" ,7),(8, "oros" ,8),(9, "oros" ,9),
      (10, "oros" ,0.5),(11, "oros" ,0.5),(12, "oros" ,0.5),

      (1, "copas" ,1),(2, "copas" ,2),(3, "copas" ,3),
      (4, "copas" ,4),(5, "copas" ,5),(6, "copas" ,6),
      (7, "copas" ,7),(8, "copas" ,8),(9, "copas" ,9),
      (10, "copas" ,0.5),(11, "copas" ,0.5),(12, "copas" ,0.5),

      (1, "bastos" ,1),(2, "bastos" ,2),(3, "bastos" ,3),
      (4, "bastos" ,4),(5, "bastos" ,5),(6, "bastos" ,6),
      (7, "bastos" ,7),(10, "bastos" ,10),(11, "bastos" ,11),
      (10, "bastos" ,0.5),(11, "bastos" ,0.5),(12, "bastos" ,0.5),

      (1, "espadas" ,1),(2, "espadas" ,2), (3, "espadas" ,3),
      (4, "espadas" ,4),(5, "espadas" ,5), (6, "espadas" ,6),
      (7, "espadas" ,7),(10, "espadas" ,10), (11, "espadas" ,11),
      (10, "espadas" ,0.5),(11, "espadas" ,0.5),(12, "espadas" ,0.5)]

# Hacer lista de jugador max 8
Jugadores=[]
Salir=False
while not Salir:
    Nombre=input("Escriu el nom d'un jugador: ")
    if Nombre.isalnum()==True and Nombre[0].isalpha()==True:
        Jugadores.append({Nombre})
        Respuesta=input("Vols inscriure un altre jugador? (Si o No) ")
        if Respuesta=="No":
            Salir=True
    elif Nombre.isalnum()==False:
        print("El nom només pot ser de lletras i números i no pot contenir espais.")
    elif Nombre[0].isalpha()==False:
        print("El primer caràcter del nom ha de ser una lletra.")
print(Jugadores)

# Escoger carta aleatoria por jugador para orden prioridad
# jugadores=[] ordenado de mayor a menor
# diccionario con tuplas de cada jugador clave nombre valor cartas
# Bucle nueva mano 0
# Bucle mano por jugador 1
# Subbucle mano por jugador 2
# Fin bucle mano por jugador 1
# Fin subbucle mano por jugador 2