```
docker compose

#dentro la cartella docker-compose
docker-compose up --build

#per vedere i container creati
docker ps -a

#Per mysql creare le tabelle

###post dentro mysql-follow
create database dsbd_follow;
use dsbd_follow;
create table follow( user_id integer, follow_id integer, PRIMARY KEY(user_id,follow_id))

####user dentro mysql-login
create database dsbd_login;
use dsbd_login;
create table user( id integer PRIMARY KEY AUTO_INCREMENT, username varchar(255), password varchar(255),counter_post integer);

#in mongo
#il database: use dsbd_post
db.createCollection("post")
```
