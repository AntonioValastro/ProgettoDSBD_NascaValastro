from flask import Flask
from flask import request
from flask import jsonify
from flask import session
import mysql.connector
import socket
import json
from datetime import timedelta
from fix_nginx import ReverseProxied
from netifaces import interfaces, ifaddresses, AF_INET

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.secret_key = "dsbd"
app.permanent_session_lifetime = timedelta(minutes=50)
userflag=None
healthy = True
def get_addresses():
    strret = ""
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        strret += '%s: %s\n' % (ifaceName, ', '.join(addresses))
    return strret
    

@app.route("/ping")
def ping():
    if healthy:
        return "pong"
    else:
        return "not healthy", 500

@app.route("/login", methods=['GET', 'POST'])
def login():
    if healthy:
    	mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
    	mycursor=mydb.cursor()
    	mycursor.execute("select * from user where username = '" + request.args.get('username')+"' and password = '"+ request.args.get('password')+"'")
    	myresult=mycursor.fetchone()
    	if myresult != None:
    		session['userId']=myresult[0]
    		return "1"
    	else:
    		return "0"
    else:
        return "not healthy", 500

@app.route("/registrazione", methods=['GET', 'POST'])
def registrazione():
    if healthy:
    	mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
    	username=request.args.get('username')
    	password=request.args.get('password')
    	mycursor = mydb.cursor()
    	sql = "INSERT INTO user (username, password,counter_post) VALUES (%s, %s,0)"
    	val = (username, password)
    	mycursor.execute(sql, val)
    	mydb.commit()
    	return "Registrazione effettuata con successo! Adesso puoi fare il login"
    else:
        return "not healthy", 500

@app.route("/flag", methods=['GET', 'POST'])
def flag():
	if healthy:
		if session['userId'] != None:
			return str(session['userId'])
		else:
			return "null"
	else:
		return "not healthy", 500

@app.route("/user", methods=['GET', 'POST'])
def user():
	print("user FUnction")
	if healthy:
		return "adminResponse/user"
	else:
		return "not healthy", 500	
		
@app.route("/getUsername", methods=['GET', 'POST'])
def getUsername():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
		mycursor=mydb.cursor(dictionary=True)
		mycursor.execute("select username from user where id ="+  request.args.get('id'))
		myresult=mycursor.fetchone()
		return json.dumps(myresult)		
	else:
		return "not healthy", 500
@app.route("/getId", methods=['GET', 'POST'])
def getId():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
		mycursor=mydb.cursor(dictionary=True)
		mycursor.execute("select id from user where username = '"+  request.args.get('username')+"'")
		myresult=mycursor.fetchone()
		if myresult != None:
			return json.dumps(myresult)
		else:
			return "-1"
	else:
		return "not healthy", 500
@app.route("/incCounter", methods=['GET', 'POST'])
def incCounter():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
		mycursor=mydb.cursor(dictionary=True)
		#faccio una update nella tabel
		sql = "UPDATE user SET counter_post = counter_post+1 WHERE id ="+ request.args.get('id')
		mycursor.execute(sql)
		mydb.commit()
		return "1"
	else:
		return "-1"

@app.route("/decCounter", methods=['GET', 'POST'])
def decCounter():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
		mycursor=mydb.cursor(dictionary=True)
		#faccio una update nella tabel
		sql = "UPDATE user SET counter_post = counter_post-1 WHERE id ="+ request.args.get('id')
		mycursor.execute(sql)
		mydb.commit()
		if mycursor.rowcount != 0:
			return "1"
		else:
			return "-1"		
	else:
		return -1	
		
@app.route("/allUsers", methods=['GET', 'POST'])
def allUsers():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-login",user="root",password="pwd",database="dsbd_login")
		mycursor=mydb.cursor(dictionary=True)
		mycursor.execute("select id,username from user")
		myresult=mycursor.fetchall()
		return json.dumps(myresult)
	else:
		return "not healthy", 500
@app.route("/break")
def set_not_healthy():
    global healthy
    healthy = False
    return f"{get_addresses()} This ms is now set to be not healthy"

@app.route("/")
def count():
    #redis.incr('counter')
    strret = "" #get_addresses()
    strret += "Count is "
    return strret

if __name__ == "__main__":
    app.run(host="0.0.0.0")

