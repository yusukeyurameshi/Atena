create table menu(
    id_menu integer primary key autoincrement,
    name text not null,
    url text
);

insert into menu (name) values ('FSDR');
insert into menu (name) values ('ExaScale');

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id_user INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

insert into user (username, password) values ('admin','admin');

DROP TABLE IF EXISTS region;

CREATE TABLE REGIONS (
  ID_REGION INTEGER PRIMARY KEY AUTOINCREMENT,
  REGION TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS COMPARTMENTS;

CREATE TABLE COMPARTMENTS (
  ID_COMPARTMENT INTEGER PRIMARY KEY AUTOINCREMENT,
  OCID TEXT UNIQUE NOT NULL,
  NAME TEXT NOT NULL,
  STATUS TEXT NOT NULL
);