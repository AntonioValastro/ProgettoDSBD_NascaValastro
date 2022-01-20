
```
COMANDI DA LANCIARE
k8s

minikube start --memory=4096 --vm-driver=docker
eval $(minikube docker-env)
docker build -t login-stateless:v1 pythonuser
docker build -t login-frontend:v1 frontend
docker build -t post-stateless:v1 pythonpost
docker build -t follow-stateless:v1 pythonfollow
minikube addons enable ingress
```

```
#Nella cartella principale
kubectl apply -f k8s

#spostarsi nella cartella k8s
kubectl apply -f mongo
kubectl apply -f prometheus --> prima bisogna creare un namespace con il nome di monitoring e poi lanciare il comando

#lanciare interfaccia browser
minikube service --namespace=monitoring grafana
minikube service --namespace=monitoring prometheus
minikube service mongo-express-service

#monitorare i container dei due namespace
watch -n 0.2 kubectl get all
watch -n 0.2 kubectl get all --namespace=monitoring
```

```
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
