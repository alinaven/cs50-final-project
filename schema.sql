CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL, apiurl TEXT NOT NULL, urlconfig TEXT NOT NULL, source TEXT NOT NULL, pricetable TEXT NOT NULL, pricefield TEXT NOT NULL, nametable TEXT NOT NULL, namefield TEXT NOT NULL, amounttable TEXT NOT NULL, amountfield TEXT NOT NULL, picturetable TEXT NOT NULL, picturefield TEXT NOT NULL);
INSERT INTO customers (name, suffix, apiurl, urlconfig, source, pricetable, pricefield, nametable, namefield, amounttable, amountfield, picturetable, picturefield) VALUES ("Intratuin", "intratuin", 'intratuin-api', '', 'data_intratuin.txt', '', '', '', '', '', '', '', '');
INSERT INTO customers (name, suffix, apiurl, urlconfig, source, pricetable, pricefield, nametable, namefield, amounttable, amountfield, picturetable, picturefield) VALUES ("Het Oosten", "het_oosten", 'oosten-api', '', 'data_het_oosten.txt', '', '', '', '', '', '', '', '');

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);
INSERT INTO users (username, password) VALUES ("Alina", "kasdifucy482!");
INSERT INTO users (username, password) VALUES ("Josephine", "uyqwerndf7566#");