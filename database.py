# -*- coding: cp1251 -*-

import sqlite3
import datetime

with sqlite3.connect('database.db') as db:
    cur = db.cursor()

    def newuser(userid):
        cur.execute(" INSERT INTO users (userid, name, costs, ta, datereg, lim, lastuse) VALUES(?, ?, ?, ?, ?, ?, ?) ", (userid, "", 0, 0, str(datetime.datetime.today()).replace(str(datetime.datetime.today()).split(".")[1], ""), 100, str(datetime.datetime.today()).split(" ")[0].replace("-", "")))
        return db.commit()

    def check(userid):
        user = cur.execute(" SELECT * FROM users WHERE userid=? ", (userid,)).fetchall()
        return bool(len(user))

    def setname(userid, name):
        cur.execute(" UPDATE users SET name=? WHERE userid=?", (name, userid))
        return db.commit()

    def setcosts(userid, costs):
        cur.execute(" UPDATE users SET costs=? WHERE userid=?", (costs, userid))
        return db.commit()

    def setta(userid, ta):
        cur.execute(" UPDATE users SET ta=? WHERE userid=?", (ta, userid))
        return db.commit()

    def setlimit(userid, lastuse):
        cur.execute(" UPDATE users SET lim=? WHERE userid=?", (lastuse, userid))
        return db.commit()

    def setlastuse(userid, lastuse):
        cur.execute(" UPDATE users SET lastuse=? WHERE userid=?", (lastuse, userid))
        return db.commit()

    def getfullinfo(userid):
        name = cur.execute(" SELECT name FROM users WHERE userid=? ", (userid,)).fetchone()
        costs = cur.execute(" SELECT costs FROM users WHERE userid=? ", (userid,)).fetchone()
        ta = cur.execute(" SELECT ta FROM users WHERE userid=? ", (userid,)).fetchone()
        datereg = cur.execute(" SELECT datereg FROM users WHERE userid=? ", (userid,)).fetchone()
        lim = cur.execute(" SELECT lim FROM users WHERE userid=? ", (userid,)).fetchone()
        lastuse = cur.execute(" SELECT lastuse FROM users WHERE userid=? ", (userid,)).fetchone()
        return name[0], costs[0], ta[0], datereg[0], lim[0], lastuse[0]
