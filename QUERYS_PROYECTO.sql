/* 1 */
WITH MyRowSet AS (select idparticipante,carta_inicial,count(carta_inicial) as "usos",ROW_NUMBER() OVER (PARTITION BY idparticipante) AS "primera_carta" from turnos group by idparticipante,carta_inicial) SELECT * FROM MyRowSet WHERE Primera_carta = 1;
/* 2 */
select nombre,max(apuesta),idpartida from (select case when username is not null then usuario.username else descripcion end as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username) tabla where (apuesta,idpartida) in (select max(turnos.apuesta),partida.idpartida as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by max(turnos.apuesta) desc) group by idpartida;
/* 3 */
select nombre,min(apuesta),idpartida from (select case when username is not null then usuario.username else descripcion end as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username) tabla where (apuesta,idpartida) in (select min(turnos.apuesta),partida.idpartida as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by min(turnos.apuesta) desc) group by idpartida;
/* 5 */
select distinct bot.descripcion,partida.ganador_partida, truncate(((2/sum(partida.idpartida))*100),2) as porcentaje from partida inner join participante on partida.ganador_partida=participante.id_participante inner join jugador on participante.id_jugador=jugador.idjugador inner join bot on jugador.idbot=bot.idbot where bot.idbot is not null;
/* 11 */
select avg(t.apuesta) as "Media", p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida group by idpartida;
/* 12 */
select distinct u.*,apuesta , max(t.numero_turno) as 'trurno_max', pd.idpartida from usuario u inner join jugador j on u.idusuario = j.idusuario inner join participante p on j.idjugador = p.id_jugador inner join turnos t on p.id_participante = t.idparticipante inner join partida pd on pd.idpartida = t.idpartida group by idpartida,idparticipante -- having numero_turno in  (select max(numero_turno) from turnos group by idpartida) order by t.idpartida asc,idparticipante asc, numero_turno asc
;
/* 13 */
select count(carta_inicial) AS numero_de_cartas, sum(valor) AS valor_total, idpartida AS partida from turnos, cartas where carta_inicial=idcartas group by idpartida;