DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL);
INSERT INTO customers (name, suffix) VALUES ("Intratuin", "intratuin");
INSERT INTO customers (name, suffix) VALUES ("Het Oosten", "het_oosten");