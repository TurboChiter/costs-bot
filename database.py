# -*- coding: cp1251 -*-

import psycopg2
import datetime

try:
	with psycopg2.connect('postgres://uqxzgefkdphtqj:321bf4ba81d9b75c0304e60ee92ac079209316f338d4db667e26deca1403a75e@ec2-54-170-90-26.eu-west-1.compute.amazonaws.com:5432/d21ag1m9ig782u') as db:
	    cur = db.cursor()

	    def newuser(userid):
	        cur.execute(" INSERT INTO users (userid, name, costs, ta, datereg, lim, lastuse) VALUES(%s, %s, %s, %s, %s, %s, %s) ", (userid, "", 0, 0, str(datetime.datetime.today()).replace(str(datetime.datetime.today()).split(".")[1], ""), 100, str(datetime.datetime.today()).split(" ")[0].replace("-", "")))
	        return db.commit()

	    def check(userid):
	        user = cur.execute(f" SELECT * FROM users WHERE userid={userid} ")
	        user = cur.fetchall()
	        return bool(len(user))

	    def setname(userid, name):
	        cur.execute(" UPDATE users SET name=%s WHERE userid=%s", (name, userid))
	        return db.commit()

	    def setcosts(userid, costs):
	        cur.execute(" UPDATE users SET costs=%s WHERE userid=%s", (costs, userid))
	        return db.commit()

	    def setta(userid, ta):
	        cur.execute(" UPDATE users SET ta=%s WHERE userid=%s", (ta, userid))
	        return db.commit()

	    def setlimit(userid, lastuse):
	        cur.execute(" UPDATE users SET lim=%s WHERE userid=%s", (lastuse, userid))
	        return db.commit()

	    def setlastuse(userid, lastuse):
	        cur.execute(" UPDATE users SET lastuse=%s WHERE userid=%s", (lastuse, userid))
	        return db.commit()

	    def getfullinfo(userid):
	        name = cur.execute(f" SELECT name FROM users WHERE userid={userid} ")
	        name = cur.fetchone()
	        costs = cur.execute(f" SELECT costs FROM users WHERE userid={userid} ")
	        costs = cur.fetchone()
	        ta = cur.execute(f" SELECT ta FROM users WHERE userid={userid} ")
	        ta = cur.fetchone()
	        datereg = cur.execute(f" SELECT datereg FROM users WHERE userid={userid} ")
	        datereg = cur.fetchone()
	        lim = cur.execute(f" SELECT lim FROM users WHERE userid={userid} ")
	        lim = cur.fetchone()
	        lastuse = cur.execute(f" SELECT lastuse FROM users WHERE userid={userid} ")
	        lastuse = cur.fetchone()
	        return name[0], costs[0], ta[0], datereg[0], lim[0], lastuse[0]
except Exception as ex:
	print("[ERROR] --------------- [ERROR]")
	print(ex)
	print("[ERROR] --------------- [ERROR]")
