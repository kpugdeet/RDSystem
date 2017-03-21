import web
import json
import numpy as np
from pymongo import MongoClient
from rbm import RBM
from ReadWriteLock import ReadWriteLock

urls = (
    "/query", "query",
    "/update", "update",
    "/train", "train"
)
app = web.application(urls, globals())

rbm = RBM()
rw = ReadWriteLock()

class query:
    def __init__(self):
        self.userPref = []

    def POST(self):
        data = json.loads(web.data())
        client = MongoClient()
        db = client.data
        usersDB = db.users

        # Get user preference list
        items = usersDB.find_one({"_id": data['userID']})
        if items is not None:
            for item in items["items"]:
                self.userPref.append([float(x) for x in item["itemValue"].split(",")])

        # Make recommendation list
        rankResult = rbm.calRanking(data['metaCard'], np.array(self.userPref))

        # Return result in json
        web.header('Content-Type', 'application/json')
        return json.dumps(rankResult)

class update:
    def __init__(self):
        self.output = {"status": "Update Done"}

    def POST(self):
        data = json.loads(web.data())
        client = MongoClient()
        db = client.data
        usersDB = db.users
        itemsDB = db.items

        # Check user already exist
        items = usersDB.find_one({"_id": data['userID']})
        if items is None:
            items = []
            exist = False
        else:
            items = items["items"]
            exist = True

        for tmp in data["items"]:
            # Insert to items collection
            item = itemsDB.find_one({"_id": tmp['itemID']})
            if item is None:
                distri = rbm.calDistri(tmp["itemDes"])[0]
                itemsDB.insert({"_id": tmp["itemID"], "itemDes": tmp["itemDes"], "itemValue": distri})
            else:
                distri = item["itemValue"]

            if not any(d["_id"] == tmp["itemID"] for d in items):
                items.append({"_id": tmp["itemID"], "itemDes": tmp["itemDes"], "itemValue": distri})

        # Insert to users collection
        if exist:
            usersDB.update({"_id": data['userID']}, {"items": items}, upsert=True)
        else:
            usersDB.insert({"_id": data['userID'], "items": items})

        # Return status
        return self.output

class train:
    def __init__(self):
        self.output = {"status": "Train Done"}
        self.itemID = []
        self.itemDes = []

    def POST(self):
        rw.acquire_write()
        try:
            client = MongoClient()
            db = client.data
            usersDB = db.users
            itemsDB = db.items

            # Training new value for each item
            for row in itemsDB.find():
                self.itemID.append(row["_id"])
                self.itemDes.append(row["itemDes"])

            # Train
            itemValue = rbm.train(self.itemDes)

            # Write back to db
            for i in range(len(self.itemID)):
                print(i)
                itemsDB.update({"_id": self.itemID[i]}, {"$set": {"itemValue": itemValue[i]}}, upsert=True)
                usersDB.update({"items": {"$elemMatch": {"_id": self.itemID[i]}}}, {"$set": {"items.$.itemValue": itemValue[i]}}, multi=True, upsert=True)
        finally:
            rw.release_write()

        # Return status
        return self.output

if __name__ == "__main__":
    app.run()