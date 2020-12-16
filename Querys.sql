-- 1. Mostrar la carta inicial más repetida por cada jugador. (Mostrar nombre jugador y carta)

with MyRowSet as 
(select usuario.username 'Nombre',carta_inicial 'Carta inicial',count(carta_inicial) as 'Veces repetida',row_number() over (partition by idparticipante) as 'primera_carta' from turnos
inner join usuario on usuario.idusuario=turnos.idparticipante
group by idparticipante,carta_inicial)
select * from MyRowSet where Primera_carta = 1;

-- 2. Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)

select Nombre,max(apuesta) 'Apuesta mínima',idpartida 'ID partida' from
(select case when username is not null then usuario.username else descripcion end
as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username)
tabla where (apuesta,idpartida) in
(select max(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by max(turnos.apuesta) desc)
group by idpartida
order by idpartida;

-- 3. Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)  *FALTA ACABAR*
 
select Nombre,min(apuesta) 'Apuesta mínima',idpartida 'ID partida' from
(select case when username is not null then usuario.username else descripcion end
as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username)
tabla where (apuesta,idpartida) in
(select min(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by min(turnos.apuesta) desc)
group by idpartida
order by idpartida;
 
-- 4. Ratio  de turnos ganados por jugador en cada partida (en porcentaje %). (Mostrar columna nombre jugador, nombre partida, y la nueva columna para el ratio "porcentaje %")

-- 5. Porcentaje de partidas ganadas por bots en general. (Nueva columna "porcentaje %") *FALTA ACABAR*

select distinct bot.descripcion 'Nombre',partida.ganador_partida 'ID ganador',truncate(((2/sum(partida.idpartida))*100),2) 'Porcentaje' from partida
inner join participante on partida.ganador_partida=participante.id_participante
inner join jugador on participante.id_jugador=jugador.idjugador
inner join bot on jugador.idbot=bot.idbot where bot.idbot is not null;

-- 6. Mostrar los datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media de puntos de las partidas ganadas totales.

select usuario.idusuario 'ID jugador',usuario.username 'Nombre',partida.duracion 'Duración partida' from usuario
inner join jugador on jugador.idusuario=usuario.idusuario
inner join participante on participante.id_jugador=jugador.idjugador
inner join partida on partida.idpartida=participante.id_partida
where partida.ganador_partida=usuario.idusuario
union
select bot.idbot,bot.descripcion,partida.duracion from bot
inner join jugador on jugador.idbot=bot.idbot
inner join participante on participante.id_jugador=jugador.idjugador
inner join partida on partida.idpartida=participante.id_partida
where partida.ganador_partida=bot.idbot
order by 'ID jugador' asc;

-- 7. Cuántas rondas se ganan en cada partida según el palo. (Ejemplo: Partida 1 - 5 rondas - Bastos como carta inicial)

-- 8. Cuantas rondas gana la banca en cada partida.

-- 9. Cuántos usuarios han sido la banca en

-- 10. Partida con la puntuación más alta final de todos los jugadores. (Mostrar nombre jugador, nombre partida, así como añadir una columna nueva en la que diga si ha ganado la partida o no)

-- 11. Calcular la apuesta media por partida.

select avg(t.apuesta) 'Media',p.idpartida from turnos t
inner join partida p on p.idpartida=t.idpartida
group by idpartida;

-- 12. Mostrar los datos de los usuarios que no son bot, así como cual ha sido su última apuesta en cada partida que ha jugado.

select distinct u.*,apuesta,max(t.numero_turno) 'Turno máximo',pd.idpartida from usuario u
inner join jugador j on u.idusuario = j.idusuario
inner join participante p on j.idjugador = p.id_jugador
inner join turnos t on p.id_participante = t.idparticipante
inner join partida pd on pd.idpartida = t.idpartida
group by idpartida,idparticipante;

-- 13. Calcular el valor total de las cartas y el numero total de cartas que se han dado en la partida. (Por ejemplo, en la partida se han dado 50 cartas y el valor total de las cartas es 47,5)

select count(carta_inicial) 'Número de cartas',sum(valor) 'Valor total',idpartida 'ID partida' from turnos,cartas
where carta_inicial=idcartas
group by idpartida;

-- 14. Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5. (Ejemplo: Rafa tenia 20 puntos, en la ronda 5 tiene 15, tiene -5 puntos de diferencia)
