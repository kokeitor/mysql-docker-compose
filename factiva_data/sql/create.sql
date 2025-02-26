drop table if exists clientes;

create table clientes(
 id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id) 
);
ALTER TABLE clientes AUTO_INCREMENT=1;