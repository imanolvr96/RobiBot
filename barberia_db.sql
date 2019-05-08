#	---	CREACION DE BASE DE DATOS ----------------------------------
DROP DATABASE IF EXISTS barberia_bd;
CREATE DATABASE barberia_bd;
USE barberia_bd;

#	---	CREACION DE TABLAS ----------------------------------
CREATE TABLE horario (
	id_horario smallint NOT NULL PRIMARY KEY,
	horas TIME,
	plazas smallint #las plazas son para posibles incrementos a la hora de meter otro barbero
);

CREATE TABLE cita (
	id_cita smallint NOT NULL AUTO_INCREMENT PRIMARY KEY,
	fecha DATE,
	hora TIME,
	telefono VARCHAR(9)
);

#	---	CREACION DE INSERT ----------------------------------
#	HORARIO DE MAÑANA
INSERT INTO horario VALUES (0, "10:00:00", 1);
INSERT INTO horario VALUES (1, "10:30:00", 1);
INSERT INTO horario VALUES (2, "11:00:00", 1);
INSERT INTO horario VALUES (3, "11:30:00", 1);
INSERT INTO horario VALUES (4, "12:00:00", 1);
INSERT INTO horario VALUES (5, "12:30:00", 1);
INSERT INTO horario VALUES (6, "13:00:00", 1);
INSERT INTO horario VALUES (7, "13:30:00", 1);

#	HORARIO DE TARDE
INSERT INTO horario VALUES (8, "16:00:00", 1);
INSERT INTO horario VALUES (9, "16:30:00", 1);
INSERT INTO horario VALUES (10, "17:00:00", 1);
INSERT INTO horario VALUES (11, "17:30:00", 1);
INSERT INTO horario VALUES (12, "18:00:00", 1);
INSERT INTO horario VALUES (13, "18:30:00", 1);
INSERT INTO horario VALUES (14, "19:00:00", 1);
INSERT INTO horario VALUES (15, "19:30:00", 1);

#	PRUEBA DE CITA
#INSERT INTO cita VALUES (0, "0000-00-00","00:00:00", "000000000");
COMMIT;

#	---	CREACION DE CONSULTAS ----------------------------------
select * FROM horario;

select fecha, hora FROM cita;