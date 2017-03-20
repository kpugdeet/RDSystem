from pymongo import MongoClient

# Initial DB
client = MongoClient()
db = client.data
users = db.users

items = []

for itemID in range(10):
    items.append({"id": itemID, "itemDes": 'Des'+str(itemID), "itemValue": '1,1,1,'+str(itemID)})

for userID in range(10):
    users.insert({"_id": userID, "items": items})