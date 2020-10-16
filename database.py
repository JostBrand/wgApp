# This Python file uses the following encoding: utf-8

if __name__ == "__main__":
     main()


import sqlite3 as sl
import datetime

# Tasks are assigned by calendar week
date = datetime.date.today()
NrWeek = date.isocalendar()[1]

import sqlite3

dbname = 'wg.db'
priceCoffe= 0.35

def startButton():
    return None

def getRfidTag():
        grabbing = True
        if grabbing == True:
            return 2
        else:
            return 0

class cDB():
    def __init__(self):
        self.CoffeeBeans = 100

    def checkCoffeBeans(self):
        return None
    def setupDB(self):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            GroupNr INTEGER,
            RfidTag INTEGER,
            Amount REAL,
            CleaningMilkCounter INTEGER,
            CleaningFullCounter INTEGER,
            CleaningLime INTEGER
        );
    """)
        conn.commit()
        conn.close()

    def addWG(self):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'INSERT INTO USER (id, name, GroupNr,RfidTag,Amount,CleaningMilkCounter,CleaningFullCounter,CleaningLime) values(?, ?, ?,?,?,0,0,0)'
        data = [
    (1, 'Jost', 1,2,0),
    (2, 'Alex', 1,0,0),
    (3, 'Jarno', 2,0,0),
    (4, 'Miriem', 2,0,0),
    (5, 'Christan', 3,0,0),
    (6, 'Amir', 3,0,0),
    (7, 'Jonas', 4,0,0),
    (8, 'Sahron', 4,0,0),
    (9, 'Tij', 5,0,0),
    (10, 'Felix', 5,0,0),
    (11, 'Kira', 6,0,0)
]
        c.executemany(sql,data)
        conn.commit()
        conn.close()

    def getUserCount(self):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'SELECT COUNT(*) FROM USER'
        c.execute(sql)
        result = c.fetchone()[0]
        conn.commit()
        conn.close()
        return result

    def getAccountBalance(self,RfidTag):
       conn = sqlite3.connect(dbname)
       c = conn.cursor()
       sql_get = 'SELECT Amount FROM USER WHERE RfidTag=={}'.format(RfidTag)
       c.execute(sql_get)
       result = c.fetchone()[0]
       conn.commit()
       conn.close()
       return result

    def changeAmount(self,RfidTag,charge):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql_set = 'UPDATE USER SET Amount={} WHERE RfidTag={}'.format(charge,RfidTag)
        c.execute(sql_set)
        conn.commit()
        conn.close()
        return True

    #3 Cleaning buttons
    def incCleaning(self,cleaningType,user_id):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        if cleaningType == 0:
                cleaningType = "CleaningMilkCounter"
        elif cleaningType == 1:
                cleaningType = "CleaningFullCounter"
        elif cleaningType == 2:
                cleaningType = "CleaningLime"
        else:
            return None

        sql_inc = 'UPDATE USER SET {}={}+1 WHERE id = {}'.format(cleaningType,cleaningType,user_id)
        c.execute(sql_inc)
        conn.commit()
        conn.close()
        return True

    def getFullUserDataById(self,user_id):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'SELECT * FROM USER WHERE ID={}'.format(user_id)
        result = c.execute(sql)
        for row in result:
            print(row)

    def payCoffee(self):
        print("payCoffe func")
        Tag = getRfidTag()
        if self.CoffeeBeans <= 5:
            print("CoffeBeans empty. Please refill")
            return False
        balance = self.getAccountBalance(Tag)
        if balance >= priceCoffe:
            startButton()
            self.changeAmount(Tag,balance-priceCoffe)
            return True
        else:
            #CLose Popup; balance too low
            print("Balance too low")
            return False

def main():

    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()

    print(db.getAccountBalance(2))
    db.changeAmount(2,10)
    print(db.getAccountBalance(2))
    db.payCoffee()
    db.incCleaning(2,2)
    print(db.getAccountBalance(2))
    db.getFullUserDataById(2)

def setup():
    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()
    return db
