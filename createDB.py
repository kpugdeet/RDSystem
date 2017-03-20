from pymongo import MongoClient

# Initial DB
client = MongoClient()
db = client.data
usersDB = db.users
itemsDB = db.items

items = []

for itemID in range(10):
    items.append({"_id": str(itemID), "itemDes": 'Des'+str(itemID), "itemValue": '1,1,1,'+str(itemID)})
    itemsDB.insert({"_id": str(itemID), "itemDes": 'Des'+str(itemID), "itemValue": '1,1,1,'+str(itemID)})

for userID in range(10):
    usersDB.insert({"_id": str(userID), "items": items})