from flask import Flask
from flask import request
from flask import jsonify
from flask import session
import json
import requests
import operator
from datetime import datetime
from flask_pymongo import PyMongo
import socket
from datetime import timedelta
from fix_nginx import ReverseProxied
from netifaces import interfaces, ifaddresses, AF_INET

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.secret_key = "dsbd12"
app.permanent_session_lifetime = timedelta(minutes=50)

mongodb_client = PyMongo(app, uri="mongodb://mongo:27017/dsbd_post")
db = mongodb_client.db
healthy = True
def getuser():
	api_url = "http://myproject.loc/login/flag"
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.text
	else:
		return "-1"
def getUsername(userid):
	api_url = "http://myproject.loc/login/getUsername?id="+str(userid)
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.json()
	else:
		return "-1"
		
def incCounter(userid):
	api_url = "http://myproject.loc/login/incCounter?id="+str(userid)
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.text
	else:
		return "-1"
def decCounter(userid):
	api_url = "http://myproject.loc/login/decCounter?id="+str(userid)
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.text
	else:
		return "-1"
def searchFollow(id_user,id_follow):
	api_url = "http://myproject.loc/follow/searchFollow?idUser="+str(id_user)+"&idFollow="+str(id_follow)
	response = requests.get(api_url)
	if response.text!="-1":
		return response.json()
	else:
		return "-1"
def getId(followtag):
	api_url = "http://myproject.loc/login/getId?username="+str(followtag)
	response = requests.get(api_url)
	if response.status_code == 200 and response.text!="-1":
		return response.json()
	else:
		return "-1"
def followedUsers(userId):
	api_url = "http://myproject.loc/follow/followedUsers?userId="+str(userId)
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.json()
	else:
		return "-1"
def calcPi(limit):  # Generator function
    """
    Prints out the digits of PI
    until it reaches the given limit
    """
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    decimal = limit
    counter = 0
    while counter != decimal + 1:
            if 4 * q + r - t < n * t:
                    # yield digit
                    yield n
                    # insert period after first digit
                    if counter == 0:
                            yield '.'
                    # end
                    if decimal == counter:
                            print('')
                            break
                    counter += 1
                    nr = 10 * (r - n * t)
                    n = ((10 * (3 * q + r)) // t) - 10 * n
                    q *= 10
                    r = nr
            else:
                    nr = (2 * q + r) * l
                    nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
                    q *= k
                    t *= l
                    l += 2
                    k += 1
                    n = nn
                    r = nr

@app.route("/setUser")
def setUser():
	if healthy:
		session['userId']=request.args.get('user')
		return session['userId']
	else:
		return "not healthy", 500

@app.route("/ping")
def ping():
    if healthy:
        return "poong"
    else:
        return "not healthy", 500

@app.route("/creaPost")
def creaPost():
    if healthy:
    	user = request.args.get('user')
    	followtag = request.args.get('tag')
    	if user==None:
    		return "errore di collegamento!"
    	#prima di effettuare il post devo incrementare un contatore di post inviando una richiesta al microservizio del login, perchè è lui che ha counter_post associato all'utente
    	response = incCounter(user)
    	if response == "1":
    		if followtag!="":
    			#Adesso prima di fare il post debbo controllare se posso fare il tag, cioè se sono amico con il tizio
    			id_follow = getId(followtag)
    			if id_follow=="-1":
    				response = decCounter(user)
    				return "utente taggato non esistente"
    			id_follow=id_follow['id']
    			friend=searchFollow(user,id_follow)
    			#if sono amico faccio l'inserimento
    			if friend != "-1":
    				db.post.insert_one({'titolo':request.args.get('titolo'), 'url': request.args.get('url'),'descrizione': request.args.get('descrizione'),'user':user,'data': datetime.now(),"tag":followtag})
    				return "post effettuato da: " + request.args.get('user')
    			#else se non sono amico non inserisco il post ma devo fare una transazione compensativa per annullare il counter++ che ho fatto fare al microservizio di login
    			else:
    				response = decCounter(user)
    				return "Rollback, richiamo funzione di compensazione, non sei suo follow"
    		else:
    			db.post.insert_one({'titolo':request.args.get('titolo'), 'url': request.args.get('url'),'descrizione': request.args.get('descrizione'),'user':user,'data': datetime.now(),"tag":"Null"})
    			return "post effettuato da: " + request.args.get('user')
    	else:
    		return response
    else:
        return "not healthy", 500
        
@app.route("/showPosts")
def showPosts():
    if healthy:
    	user = request.args.get('user')
    	if user==None:
    		return "errore di collegamento!"
    	cursor = db.post.find().sort("data",-1)
    	list_cur = list(cursor)
    	array_id_amici=followedUsers(user)
    	array_id_amici=str(array_id_amici).replace("'","\"")
    	array_id_amici=json.loads(array_id_amici)
    	result = []
    	selected_post=[]
    	for post in list_cur:
    		if post['user']==user:
    			selected_post.append(post)
    	for id_amico in array_id_amici:
    		for post in list_cur:
    			if str(post['user']) == str(id_amico['follow_id']):
    				selected_post.append(post)
    	for raw in selected_post:
    		diction = {}
    		diction["titolo"] = raw['titolo']
    		diction["url"] = raw['url']
    		diction["descrizione"] = raw['descrizione']
    		diction["user"] = raw['user']
    		diction["tag"] = raw['tag']
    		diction["data"] = raw['data']
    		username = getUsername(raw['user'])
    		diction.update(username)
    		result.append(diction)
    	result.sort(key=operator.itemgetter('data'),reverse=True)
    	for raw in result:
    		del raw['data']
    	string = str(result).replace("'","\"")
    	return str(string)
    else:
    	return "not healthy", 500

@app.route("/break")
def set_not_healthy():
    global healthy
    healthy = False
    return "not"

@app.route("/pi")
def pi():
	if healthy:
		calcPi(request.args.get('limit'))
		return"Post: appena calcolato pi"
	else:
		return "not healthy", 500

@app.route("/")
def func():
    return "CIAO"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

