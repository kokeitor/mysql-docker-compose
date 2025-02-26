-- Crear la tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar un cliente llamado "Jorge"
INSERT INTO clientes (name) VALUES ('Jorge');
