
-- Insertar un cliente llamado "Jorge"
truncate table reservas;
truncate table clientes;
INSERT INTO clientes (name) VALUES ('MAIZ');
INSERT INTO clientes (name) VALUES ('OJEDA');
INSERT INTO reservas (client_name) VALUES ('OJEDA');
INSERT INTO reservas (client_name) VALUES ('OJEDA');
INSERT INTO reservas (client_name) VALUES ('OJEDA');