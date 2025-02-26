
-- Insertar un cliente llamado "Jorge"
truncate table reservas;
truncate table clientes;
INSERT INTO clientes (name) VALUES ('MAIZ');
INSERT INTO clientes (name) VALUES ('OJEDA');
INSERT INTO reservas (client_name, timestamp) VALUES ('OJEDA', '2023-07-01 12:00:00');
INSERT INTO reservas (client_name, timestamp) VALUES ('OJEDA', '2023-07-01 12:01:00');
INSERT INTO reservas (client_name, timestamp) VALUES ('OJEDA', '2023-07-01 12:02:00');
INSERT INTO reservas (client_name, timestamp) VALUES ('OJEDA', '2023-07-01 12:03:00');