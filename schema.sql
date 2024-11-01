create table menu(
    id integer primary key autoincrement,
    name text not null,
    url text
);

insert into menu (name) values ('FSDR');
insert into menu (name) values ('ExaScale');

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tenancy;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

insert into user (username, password) values ('admin','admin');

CREATE TABLE tenancy (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  tenancy_ocid TEXT NOT NULL,
  user_ocid TEXT NOT NULL,
  home_region TEXT NOT NULL,
  fingerprint TEXT NOT NULL,
  pem_key TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);
