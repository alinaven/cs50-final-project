DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL, url TEXT NOT NULL, source TEXT NOT NULL);
INSERT INTO customers (name, suffix, url, source) VALUES ("Intratuin", "intratuin", 'intratuin-api', 'data_intratuin.txt');
INSERT INTO customers (name, suffix, url, source) VALUES ("Het Oosten", "het_oosten", 'oosten-api', 'data_het_oosten.txt');