# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import sqlite3 as sl
import datetime

# Tasks are assigned by calendar week
date = datetime.date.today()
NrWeek = date.isocalendar()[1]

'''
con = sl.connect('wg.db')

with con:
    response = con.execute("""SELECT COUNT(*)""")
    for row in response:
        print(len(row))



with con:
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            GroupNr INTEGER
        );
    """)
sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
data = [
    (1, 'Jost', 1),
    (2, 'Alex', 1),
    (3, 'Jarno', 2)
    (4, 'Miriam', 2)
    (5, 'Christan', 3)
    (6, 'Amir', 3)
    (7, 'Jonas', 4)
    (8, 'Sahron', 4)
    (9, 'Tij', 5)
    (10, 'Felix', 5)
    (11, 'Kira', 6)
]
with con:
    con.executemany(sql, data)

with con:
    data = con.execute("SELECT * FROM USER WHERE GroupNr == 4")
    for row in data:
        print(row)

'''





