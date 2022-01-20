import os
import time
from random import seed
from random import random
import math

"""Questo codice è stato usato per simulare l'uso del servizio da parte di alcuni utenti, e dunque poter ricavare delle statistiche
    derivanti da quest uso, abbiamo chiamato la route "pi" con l'unico scopo di fargli fare del calcolo e utilizzare risorse CPU"""

post_request = "curl http://localhost:5000/post/pi?limit="
user_request = "curl http://localhost:5000/login/pi?limit="
follow_request = "curl http://localhost:5000/follow/pi?limit="


def diff_login(counter):
    return 100000000+counter

def diff_post(counter):
    return 100000000*counter

def diff_follow(counter):
    return int(100000000+math.exp(counter))

# seed random number generator
seed(1)

time_const = 1 #s

counter = 0
while 1:

    difficulty_login = diff_login(counter)
    difficulty_post = diff_post(counter)
    difficulty_follow = diff_follow(counter)
    
    os.system(post_request+str(difficulty_post))
    os.system(post_request+str(difficulty_post))
    os.system(post_request+str(difficulty_post))
    time.sleep(time_const)
    os.system(user_request+str(difficulty_login))
    os.system(user_request+str(difficulty_login))
    os.system(user_request+str(difficulty_login))
    os.system(user_request+str(difficulty_login))
    time.sleep(time_const)
    os.system(follow_request+str(difficulty_follow))
    os.system(follow_request+str(difficulty_follow))
    os.system(follow_request+str(difficulty_follow))
    os.system(follow_request+str(difficulty_follow))
    os.system(follow_request+str(difficulty_follow))
    os.system(follow_request+str(difficulty_follow))
    value = 60
    time.sleep(value)
    print("ho aspettato "+str(value))
    counter+=1
    if(counter>20):
        break

