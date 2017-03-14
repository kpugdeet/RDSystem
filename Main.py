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
        conn = sqlite3.connect("user.db", check_same_thread=False)
        c = conn.cursor()

        # Get user preference list
        rw.acquire_read()
        try:
            for row in c.execute("SELECT itemDetail.itemValue FROM userPref JOIN itemDetail ON userPref.itemID = itemDetail.itemID "
                                 "WHERE userID = '{0}';".format(data['userID'])):
                self.userPref.append([int(x) for x in row[0].split(",")])
        finally:
            rw.release_read()

        # Make recommendation list
        rankResult = lda.calRanking(data['metaCard'], np.array(self.userPref))

        # Return result in json
        web.header('Content-Type', 'application/json')
        return json.dumps(rankResult)

class update:
    def __init__(self):
        self.output = {"status": "Update Done"}

    def POST(self):
        data = json.loads(web.data())
        conn = sqlite3.connect("user.db", check_same_thread=False)
        c = conn.cursor()

        for tmp in data["item"]:
            # Update to itemDetail db
            rw.acquire_read()
            try:
                exist = c.execute("SELECT itemID FROM itemDetail WHERE itemID = {0} LIMIT 1;".format(tmp["itemID"]))
            finally:
                rw.release_read()
            for row in exist:
                break
            else:
                rw.acquire_write()
                try:
                    c.execute("INSERT INTO itemDetail (itemID, itemDes, itemValue) VALUES ('{0}','{1}','{2}')"
                              .format(tmp['itemID'], tmp['itemDes'], lda.calDistri(tmp['itemDes'])))
                    conn.commit()
                finally:
                    rw.release_write()

            # Check data exist
            rw.acquire_read()
            try:
                exist = c.execute("SELECT userID FROM userPref WHERE userID = '{0}' and itemID = '{1}' LIMIT 1;".format(data['userID'], tmp['itemID']))
            finally:
                rw.release_read()

            # If not exist insert to db
            for row in exist:
                break
            else:
                rw.acquire_write()
                try:
                    c.execute("INSERT INTO userPref (userID, itemID) VALUES ('{0}','{1}')".format(data['userID'], tmp['itemID']))
                    conn.commit()
                finally:
                    rw.release_write()

        # Return status
        return self.output

class train:
    def __init__(self):
        self.output = {"status": "Train Done"}
        self.itemID = []
        self.itemDes = []

    def POST(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        c = conn.cursor()

        # Training new value for each item
        rw.acquire_read()
        try:
            for row in c.execute("SELECT itemID, itemDes FROM itemDetail;"):
                self.itemID.append(row[0])
                self.itemDes.append(row[1])
        finally:
            rw.release_read()

        # Train
        itemValue = lda.train(self.itemID, self.itemDes)

        # Write back to db
        rw.acquire_write()
        try:
           c.executescript('drop table if exists itemDetail;')
           c.execute("CREATE TABLE itemDetail (itemID text, itemDes text, itemValue text)")
           for i in range(len(self.itemID)):
               c.execute("INSERT INTO itemDetail VALUES ('{0}','{1}','{2}');".format(self.itemID[i], self.itemDes[i], itemValue[i]))
           conn.commit()
           time.sleep(10)
        finally:
            rw.release_write()

        # Return status
        return self.output

if __name__ == "__main__":
    app.run()