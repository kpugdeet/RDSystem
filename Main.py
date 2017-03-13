import web
import json
import sqlite3
import numpy as np
from ReadWriteLock import ReadWriteLock
from LDA import LDA
import time

urls = (
    "/query", "query",
    "/update", "update",
    "/train", "train"
)
app = web.application(urls, globals())

lda = LDA()
rw = ReadWriteLock()

class query:
    def __init__(self):
        self.userPref = []

    def POST(self):
        data = json.loads(web.data())
        rw.acquire_read()
        try:
            # Get user preference list
            conn = sqlite3.connect("user.db", check_same_thread=False)
            c = conn.cursor()
            for row in c.execute("SELECT userPref.itemID, itemDetail.itemValue FROM userPref JOIN itemDetail ON userPref.itemID = itemDetail.itemID "
                                 "WHERE userID = '{0}';".format(data['userID'])):
                self.userPref.append([int(x) for x in row[1].split(",")])
            # Make recommendation list
            rankResult = lda.calRanking(data['metaCard'], np.array(self.userPref))
        finally:
            rw.release_read()

        web.header('Content-Type', 'application/json')
        return json.dumps(rankResult)

# Update when user choose new metaCard
class update:
    def __init__(self):
        self.output = {"status": "Update Done"}

    def POST(self):
        data = json.loads(web.data())
        rw.acquire_write()
        try:
            conn = sqlite3.connect("user.db", check_same_thread=False)
            c = conn.cursor()
            for row in c.execute("SELECT * FROM userPref WHERE userID = '{0}' and itemID = '{1}'".format(data['userID'], data['itemID'])):
                self.output = {"status": "Data already exist"}
                break
            else:
                c.execute("INSERT INTO userPref (userID, itemID) VALUES ('{0}','{1}')".format(data['userID'], data['itemID']))
            conn.commit()
        finally:
            rw.release_write()
        return self.output

class train:
    def __init__(self):
        self.output = {"status": "Train Done"}
        self.itemID = []
        self.itemDes = []

    def POST(self):
        rw.acquire_write()
        try:
            conn = sqlite3.connect('user.db', check_same_thread=False)
            c = conn.cursor()

            # Training new value for each item
            for row in c.execute("SELECT itemID, itemDes FROM itemDetail;"):
                self.itemID.append(row[0])
                self.itemDes.append(row[1])
            itemValue = lda.train(self.itemID, self.itemDes)

            c.executescript('drop table if exists itemDetail;')
            c.execute("CREATE TABLE itemDetail (itemID text, itemDes text, itemValue text)")
            for i in range(len(self.itemID)):
                c.execute("INSERT INTO itemDetail VALUES ('{0}','{1}','{2}');".format(self.itemID[i], self.itemDes[i], itemValue[i]))
            conn.commit()

            time.sleep(10)
        finally:
            rw.release_write()
        return self.output

if __name__ == "__main__":
    app.run()