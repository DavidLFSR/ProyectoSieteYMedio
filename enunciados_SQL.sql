-- 1. Mostrar la carta inicial más repetida por cada jugador. (Mostrar nombre jugador y carta)   *FALTA ACABAR*

select usuario.username,cartas.numero_carta 'Carta inicial',count(cartas.numero_carta) 'Veces repetida',turnos.carta_inicial 'ID carta' from turnos
inner join cartas on turnos.carta_inicial=cartas.idcartas
inner join participante on participante.id_participante=turnos.idparticipante
inner join jugador on jugador.idjugador=participante.id_jugador
inner join usuario on usuario.idusuario=jugador.idusuario
group by usuario.username,cartas.numero_carta;

-- 2. Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)  *FALTA ACABAR*

select nombre,max(apuesta),idpartida
from
(
select 
case 
when username is not null then usuario.username 
else descripcion 
end
as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username
) tabla
where (apuesta,idpartida) in (
select 
max(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by max(turnos.apuesta) desc
)
group by idpartida
order by idpartida;

-- 3. Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)  *FALTA ACABAR*
 
select nombre,min(apuesta),idpartida
from
(
select 
case 
when username is not null then usuario.username 
else descripcion 
end
as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username
) tabla
where (apuesta,idpartida) in (
select 
min(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by min(turnos.apuesta) desc
)
group by idpartida
order by idpartida;
 
-- 4. Ratio  de turnos ganados por jugador en cada partida (en porcentaje %). (Mostrar columna nombre jugador, nombre partida, y la nueva columna para el ratio "porcentaje %")

-- 5. Porcentaje de partidas ganadas por bots en general. (Nueva columna "porcentaje %") *FALTA ACABAR*

select ganador_partida 'Porcentaje %' from (
partida
inner join participante on partida.idpartida=participante.id_partida
inner join jugador on participante.id_jugador=jugador.idjugador
inner join bot on jugador.idbot=bot.idbot);

-- 6. Mostrar los datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media de puntos de las partidas ganadas totales.

select usuario.idusuario,usuario.username from usuario
inner join jugador on jugador.idusuario=usuario.idusuario
order by idusuario;
select bot.idbot,bot.descripcion from bot
inner join jugador on jugador.idbot=bot.idbot
order by idbot;

-- 7. Cuántas rondas se ganan en cada partida según el palo. (Ejemplo: Partida 1 - 5 rondas - Bastos como carta inicial)

-- 8. Cuantas rondas gana la banca en cada partida.

-- 9. Cuántos usuarios han sido la banca en

-- 10. Partida con la puntuación más alta final de todos los jugadores. (Mostrar nombre jugador, nombre partida, así como añadir una columna nueva en la que diga si ha ganado la partida o no)

-- 11. Calcular la apuesta media por partida.

-- 12. Mostrar los datos de los usuarios que no son bot, así como cual ha sido su última apuesta en cada partida que ha jugado.

-- 13. Calcular el valor total de las cartas y el numero total de cartas que se han dado en la partida. (Por ejemplo, en la partida se han dado 50 cartas y el valor total de las cartas es 47,5)

-- 14. Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5. (Ejemplo: Rafa tenia 20 puntos, en la ronda 5 tiene 15, tiene -5 puntos de diferencia)
