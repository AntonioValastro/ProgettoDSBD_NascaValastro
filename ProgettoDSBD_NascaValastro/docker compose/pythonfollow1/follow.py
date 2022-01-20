from flask import Flask
from flask import request
from flask import jsonify
from flask import session
import json
import requests
import subprocess
import mysql.connector
from fix_nginx import ReverseProxied
from netifaces import interfaces, ifaddresses, AF_INET

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.secret_key = "dsbd123"

#mongodb_client = PyMongo(app, uri="mongodb://172.17.0.8:27017/todo_db")
#db = mongodb_client.db

healthy = True
def getAlluser():
	api_url = "http://user:5000/allUsers"
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.json()
	else:
		return "-1"
def followedUser(userId):
	mydb=mysql.connector.connect(host="mysql-post",user="root",password="pwd",database="dsbd_follow")
	mycursor=mydb.cursor(dictionary=True)
	#tonra tutti i miei amici
	mycursor.execute("select follow_id from follow where user_id ="+ str(userId))
	myresult=mycursor.fetchall()
	if myresult != None:
		return json.dumps(myresult)
	else:
		return "-1"

@app.route("/setUser")
def setUser():
	if healthy:
		session['userId']=request.args.get('user')
		return session['userId']
	else:
		return "not healthy", 500
@app.route("/showUsers")
def showUsers():
	if healthy:
		users= getAlluser()
		utenteCorrente=request.args.get('user')
		array_id_amici=followedUser(request.args.get('user'))
		if(array_id_amici=="-1"):
			for user in users:
				if  str(user['id']) == str(utenteCorrente):
					users.remove(user)
		else:
			array_id_amici=str(array_id_amici).replace("'","\"")
			array_id_amici=json.loads(array_id_amici)
			for user in users:
				if  str(user['id']) == utenteCorrente:
					users.remove(user)
			for id_user in array_id_amici:
				for user in users:
						if str(user['id']) == str(id_user['follow_id']):
							users.remove(user)
							break
					
		return json.dumps(users)																
	else:
		return "not healthy", 500
@app.route("/searchFollow", methods=['GET', 'POST'])
def searchFollow():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-post",user="root",password="pwd",database="dsbd_follow")
		mycursor=mydb.cursor(dictionary=True)
		mycursor.execute("select follow_id from follow where user_id ="+  request.args.get('idUser') + " and follow_id=" + request.args.get('idFollow'))
		myresult=mycursor.fetchone()
		if myresult != None:
			return json.dumps(myresult)
		else:
			return "-1"
	else:
		return "not healthy", 500

@app.route("/userFollowed", methods=['GET', 'POST'])
def userFollowed():
	if healthy:
		mydb=mysql.connector.connect(host="mysql-post",user="root",password="pwd",database="dsbd_follow")
		mycursor=mydb.cursor(dictionary=True)
		#tonra tutti i miei amici
		mycursor.execute("select follow_id from follow where user_id ="+  request.args.get('userId'))
		myresult=mycursor.fetchall()
		if myresult != None:
			return json.dumps(myresult)
		else:
			return "-1"
	else:
		return "not healthy", 500
@app.route("/addFollow", methods=['GET', 'POST'])
def addFollow():
	if healthy:
		#insert
		mydb = mysql.connector.connect(host="mysql-post",user="root",password="pwd",database="dsbd_follow")
		mycursor = mydb.cursor()
		sql = "INSERT INTO follow VALUES ('"+request.args.get('user')+"','"+request.args.get('targetId')+"');"
		mycursor.execute(sql)
		mydb.commit()
		return "Friends!"
	else:
		return "not healthy", 500

@app.route("/ping")
def ping():
    if healthy:
    	return "pongFollow"
    else:
        return "not healthy", 500

@app.route("/pippo")
def pippo():
    if healthy:
    	#pippo=1
    	#todos = db.todos.find_one({"_id": 2})
    	return "pippo"
    else:
        return "not healthy", 500

@app.route("/break")
def set_not_healthy():
    global healthy
    healthy = False
    return "not"

@app.route("/")
def func():
    return "CIAO da proFollow"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

