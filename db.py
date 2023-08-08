import sqlite3

connection = sqlite3.connect('sportdata.db')
with open ('sport_data.sql') as f:
    connection.executescript(f.read())
connection.commit()
connection.close()