import sqlite3

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()

def create_table(): # user club table
    c.execute('CREATE TABLE IF NOT EXISTS userClubs (userID, clubID INT, season VARCHAR(5), balance INT)')

def create_table2(): #player and User club linking table
    c.execute('CREATE TABLE IF NOT EXISTS clubsPlayers (clubID INT, playerID VARCHAR(8),priceWhenPacked INT) ')

def create_table3(): #club and active squad linking table
  c.execute('CREATE TABLE IF NOT EXISTS clubsActiveSquads (clubID INT,formationID INT DEFAULT NULL, player1 VARCHAR(8) DEFAULT NULL, player2 VARCHAR(8) DEFAULT NULL, player3 VARCHAR(8) DEFAULT NULL, player4 VARCHAR(8) DEFAULT NULL, player5 VARCHAR(8) DEFAULT NULL, player6 VARCHAR(8) DEFAULT NULL, player7 VARCHAR(8) DEFAULT NULL, player8 VARCHAR(8) DEFAULT NULL, player9 VARCHAR(8) DEFAULT NULL, player10 VARCHAR(8) DEFAULT NULL, player11 VARCHAR(8) DEFAULT NULL) ')

def create_table4(): #formations table
  c.execute('CREATE TABLE IF NOT EXISTS formations (formationID INTEGER PRIMARY KEY AUTOINCREMENT,DF INT(1), MF INT(1), FW INT(1))')

def addFormation(structure): #Adding formations to database
    DF = structure[0]
    MF = structure[1]
    FW = structure[2]
    c.execute("INSERT INTO formations (DF, MF, FW) VALUES(?,?,?)",(DF,MF,FW))
    conn.commit()

def delete_table():
  c.execute("DROP TABLE IF EXISTS userClubs")

def delete_table2():
  c.execute("DROP TABLE IF EXISTS clubsPlayers")

def delete_table3():
  c.execute("DROP TABLE IF EXISTS clubsActiveSquads")

def delete_table4():
  c.execute("DROP TABLE IF EXISTS formations")


def createClubsMain():
  delete_table()
  create_table()

  delete_table2()
  create_table2()

  delete_table3()
  create_table3()

  delete_table4()
  create_table4()

  addFormation('433')
  addFormation('442')
  addFormation('532')
  addFormation('523')
  addFormation('343')

  c.close()
  conn.close()

createClubsMain()