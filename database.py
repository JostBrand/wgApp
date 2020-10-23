# This Python file uses the following encoding: utf-8

import sqlite3 as sl
import datetime
import backend

# Tasks are assigned by calendar week
date = datetime.date.today()
NrWeek = date.isocalendar()[1]

import sqlite3

dbname = 'wg.db'
priceCoffe = 0.35


class cDB():
    def __init__(self):
        self.CoffeeBeans = 100

    def set(self,statement):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(statement)
        conn.commit()
        conn.close()

    # Getter for single lines
    def get(self,statement):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute(statement)
        result = c.fetchone()[0]
        conn.commit()
        return result

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
        sql = 'INSERT INTO USER (id, name, GroupNr,RfidTag,Amount,CleaningMilkCounter,CleaningFullCounter,CleaningLime,CoffesTaken,ReFunds) values(?, ?, ?,?,0,0,0,0,0,0)'
        data = [
    (1, 'Jost', 1,"441850866162"),
    (2, 'Alex', 1,"535544663601"),
    (3, 'Jarno', 2,"577279633739"),
    (4, 'Miriem', 2,"575681407471"),
    (5, 'OktMb', 3,"371127429628"),
    (6, 'Amir', 3,"440087554427"),
    (7, 'Jonas', 4,"576080062850"),
    (8, 'Sharon', 4,"327982457717"),
    (9, 'Tij', 5,"465768615401"),
    (10, 'Felix', 5,"438374246778"),
    (11, 'Kira', 6,"442358835477")
]
        c.executemany(sql,data)
        conn.commit()

    def getUserCount(self):
        return self.get('SELECT COUNT(*) FROM USER')

    def tagExists(self,RfidTag=None):
        if RfidTag is None:
            return False
        return self.get(f'SELECT COUNT(*) FROM USER WHERE RfidTag = {RfidTag}')
        #return self.get(f'SELECT COUNT(*) FROM USER WHERE RfidTag = {RfidTag}') != 0

    def getAccountName(self,RfidTag):
        if  not self.tagExists(RfidTag):
            return
        return self.get(f'SELECT name FROM USER WHERE RfidTag=={RfidTag}')

    def getAccountBalance(self,RfidTag):
       if not self.tagExists(RfidTag):
           return 0
       return self.get(f'SELECT Amount FROM USER WHERE RfidTag=={RfidTag}')

    def changeAmount(self,RfidTag,newVal):
        self.set(f'UPDATE USER SET Amount={newVal} WHERE RfidTag={RfidTag}')
        return True

    def incRefund(self, RfidTag):
        sql_inc = f'UPDATE USER SET ReFunds=ReFunds+1 WHERE RfidTag = {RfidTag}'
        print(sql_inc)
        self.set(sql_inc)

    #3 Cleaning buttons
    def incCleaning(self, cleaningType, RfidTag):

        if RfidTag is None:
            self.systemlogger("inCleaning failed - User ID None", "NA")
            return False
        if cleaningType == "Milk":
                cleaningType = "CleaningMilkCounter"
                self.systemlogger("Milktube Cleaned",RfidTag)
        elif cleaningType == "Full":
                cleaningType = "CleaningFullCounter"
                self.systemlogger("Full Clean",RfidTag)
        elif cleaningType == "Lime":
                cleaningType = "CleaningLime"
                self.systemlogger("Lime Clean",RfidTag)
        else:
            return None

        self.set(f'UPDATE USER SET {cleaningType}={cleaningType}+1 WHERE RfidTag = "{RfidTag}"')
        return True

    def getFullUserDataById(self, user_id):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'SELECT * FROM USER WHERE ID={}'.format(user_id)
        result = c.execute(sql)
        for row in result:
            print(row)

    def getFullDump(self):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        sql = 'SELECT * FROM USER'
        result = c.execute(sql)
        for row in result:
            print(row)

    def payCoffee(self,tag):
        print("payCoffe func")
        if self.CoffeeBeans <= 0.15:
            print("Beans empty. Please refill or check Sensor")
            return False
        balance = self.getAccountBalance(tag)
        if balance >= priceCoffe:
            newBalance = balance-priceCoffe
            self.changeAmount(tag, newBalance)
            print(f'Your new balance is {newBalance}')
            self.systemlogger("Coffee taken ", tag)

            return True
        else:
            #CLose Popup; balance too low
            print("Balance too low")
            return False

    def systemlogger(self,logmsg,tag):
        dt = datetime.datetime.now()
        with open("systemlog.txt", "a") as myfile:
            myfile.write(str(dt) + "--- action: " + logmsg + " by user: "+str(tag)+ " ("+self.getAccountName(tag)+")"+ "\n")




if __name__ == "__main__":
    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()

    print(db.getFullDump())

def setup():
    db = cDB()
    db.setupDB()

    if db.getUserCount() == 0:
        db.addWG()
        db.changeAmount("441850866162", 500)
        db.changeAmount("438374246778", 500)

    return db
