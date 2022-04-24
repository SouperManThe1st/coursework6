import sqlite3


def create_table(): # user club table
    conn = sqlite3.connect('pythonDB21.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userLogins (userID INTEGER PRIMARY KEY AUTOINCREMENT,email VARCHAR(50),firstname VARCHAR(50), password VARCHAR(50))')
    c.close()
    conn.close()

def delete_table():
    conn = sqlite3.connect('pythonDB21.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS userLogins")
    c.close()
    conn.close()



def userLoginsMain():
  delete_table()
  create_table()

userLoginsMain()