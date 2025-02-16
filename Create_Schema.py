import sqlite3
#Create and connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

#Create table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 date TEXT NOT NULL,
                 category TEXT NOT NULL,
                 amount REAL NOT NULL,
                  description TEXT
               )
                ''')
conn.commit()
conn.close()

