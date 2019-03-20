CREATE TABLE users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  token text not null);

INSERT INTO users (username, password, token) VALUES ('density', '$2y$12$6AVr2QwSrHCHvSJ7PT6.fOihmX34DrU1N4M8zPoo/RVTs/c029hSS', 'mytoken');
