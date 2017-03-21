import csv
import re
from pymongo import MongoClient

# Initial DB
client = MongoClient()
db = client.data
usersDB = db.users
itemsDB = db.items


itemData = {}
with open("./data/raw-data.csv") as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        tmp = re.sub(r'[^\w]', ' ', row[4])
        itemData[row[0]] = tmp
        itemsDB.insert({"_id": row[0], "itemDes": tmp, "itemValue": "-"})

prev = 1
items = []
with open("./data/user-info.csv") as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        if prev != int(row[0]):
            usersDB.insert({"_id": str(prev), "items": items})
            items = []
            prev = int(row[0])
            items.append({"_id": row[1], "itemDes": itemData[row[1]], "itemValue": "-"})
        else:
            items.append({"_id": row[1], "itemDes": itemData[row[1]], "itemValue": "-"})

#items = []
# for itemID in range(10):
#     items.append({"_id": str(itemID), "itemDes": 'Des'+str(itemID), "itemValue": '1,1,1,'+str(itemID)})
#     itemsDB.insert({"_id": str(itemID), "itemDes": 'Des'+str(itemID), "itemValue": '1,1,1,'+str(itemID)})
#
# for userID in range(10):
#     usersDB.insert({"_id": str(userID), "items": items})