# This Python file uses the following encoding: utf-8

import sqlite3 as sl
import datetime

# Tasks are assigned by calendar week
date = datetime.date.today()
NrWeek = date.isocalendar()[1]

import sqlite3

dbname = 'wg.db'
priceCoffe= 0.35

def systemlogger(logmsg,tag):
    dt = datetime.datetime.now()
    with open("systemlog.txt", "a") as myfile:
        myfile.write(str(dt) + "--- action: "+ logmsg + "by user: "+str(tag)+("\n"))


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
            RfidTag TEXT,
            Amount REAL,
            CleaningMilkCounter INTEGER,
            CleaningFullCounter INTEGER,
            CleaningLime INTEGER,
            CoffesTaken INTEGER,
            ReFunds INTEGER
        );
    """)
        conn.commit()
        conn.close()

    def addWG(self):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'INSERT INTO USER (id, name, GroupNr,RfidTag,Amount,CleaningMilkCounter,CleaningFullCounter,CleaningLime,CoffesTaken,ReFunds) values(?, ?, ?,?,?,?,?,?,?,?)'
        data = [
    (1, 'Jost', 1,"441850866162"  ,500.0,0,0,0,0,0),
    (2, 'Alex', 1,"535544663601"  ,0.0,0,0,0,0,0),
    (3, 'Jarno', 2,"577279633739" ,0.0,0,0,0,0,0),
    (4, 'Miriem', 2,"575681407471",0.0,0,0,0,0,0),
    (5, 'OktMb', 3,"371127429628" ,0.0,0,0,0,0,0),
    (6, 'Amir', 3,"440087554427"  ,10.0,0,0,0,0,0),
    (7, 'Jonas', 4,"576080062850" ,0.0,0,0,0,0,0),
    (8, 'Sharon', 4,"327982457717",0.0,0,0,0,0,0),
    (9, 'Tij', 5,"465768615401"   ,0.0,0,0,0,0,0),
    (10, 'Felix', 5,"438374246778",5.0,0,0,0,0,0),
    (11, 'Kira', 6,"442358835477" ,0.0,0,0,0,0,0)
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

    def tagExists(self,RfidTag=None):
        if RfidTag is None:
            return False
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'SELECT COUNT(*) FROM USER WHERE RfidTag = "{}"'.format(RfidTag)
        c.execute(sql)
        result = c.fetchone()[0]
        conn.commit()
        conn.close()
        return result != 0

    def getAccountName(self,RfidTag):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql_get = 'SELECT name FROM USER WHERE RfidTag=="{}"'.format(RfidTag)
        c.execute(sql_get)
        result = c.fetchone()[0]
        conn.commit()
        conn.close()
        return result

    def getAccountBalance(self,RfidTag):
       conn = sqlite3.connect(dbname)
       c = conn.cursor()
       sql_get = 'SELECT Amount FROM USER WHERE RfidTag=="{}"'.format(RfidTag)
       c.execute(sql_get)
       result = c.fetchone()[0]
       conn.commit()
       conn.close()
       return result

    def changeAmount(self,RfidTag,charge):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql_set = 'UPDATE USER SET Amount={} WHERE RfidTag="{}"'.format(charge,RfidTag)
        c.execute(sql_set)
        conn.commit()
        conn.close()
        return True

    #3 Cleaning buttons
    def incCleaning(self,cleaningType,user_id):

        if user_id is None:
            systemlogger("inCleaning failed - User ID None","NA")
            return False

        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        if cleaningType == "Milk":
                cleaningType = "CleaningMilkCounter"
                systemlogger("Milktube Cleaned",user_id)
        elif cleaningType == "Full":
                cleaningType = "CleaningFullCounter"
                systemlogger("Full Clean",user_id)
        elif cleaningType == "Lime":
                cleaningType = "CleaningLime"
                systemlogger("Lime Clean",user_id)
        else:
            return None

        sql_inc = f'UPDATE USER SET {cleaningType}={cleaningType}+1 WHERE id = {user_id}'
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

    def payCoffee(self,tag):
        print("payCoffe func")
        if self.CoffeeBeans <= 0.15:
            print("CoffeBeans empty. Please refill or check Sensor")
            return False
        balance = self.getAccountBalance(tag)
        if balance >= priceCoffe:
            newBalance = balance-priceCoffe
            self.changeAmount(tag,newBalance)
            print(f"Your new balance is {newBalance}")
            systemlogger("Coffee Taken",tag)
            return True
        else:
            #CLose Popup; balance too low
            print("Balance too low")
            return False


if __name__ == "__main__":
    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()

    print(db.tagExists())

def setup():
    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()
    return db
