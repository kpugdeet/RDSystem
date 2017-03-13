import sqlite3

conn = sqlite3.connect('user.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE userPref (userID text, itemID text, PRIMARY KEY (userID, itemID))")
c.execute("CREATE TABLE itemDetail (itemID text PRIMARY KEY, itemDes text, itemValue text)")

for itemID in range(10):
    c.execute("INSERT INTO itemDetail VALUES ('{0}','{1}','{2}');".format(itemID, 'des' + str(itemID), '1,1,1,'+str(itemID)))

for itemID in range(3):
    for userID in range(10):
        c.execute("INSERT INTO userPref VALUES ('{0}','{1}');".format(userID, itemID))

conn.commit()