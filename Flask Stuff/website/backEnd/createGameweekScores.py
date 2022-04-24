import sqlite3
from datetime import date
from datetime import timedelta 

def getDate(d1):
  d1 = date(int(d1[0:4]),int(d1[5:7]),int(d1[8:10]))
  return d1

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()

def createTable1(): #Results
  c.execute('CREATE TABLE IF NOT EXISTS gameweekScores (gameweekID INT, clubID INT, weekScore INT)')

def createTable2(): #Fixtures
  c.execute('CREATE TABLE IF NOT EXISTS gameweeks (gameweekID INT, windowStart DATE (12), windowEnd DATE (12))')

def createTable3():
  c.execute('CREATE TABLE IF NOT EXISTS gameweekSquads (gameweekID INT, clubID INT, player1 VARCHAR(8) DEFAULT NULL, player2 VARCHAR(8) DEFAULT NULL, player3 VARCHAR(8) DEFAULT NULL, player4 VARCHAR(8) DEFAULT NULL, player5 VARCHAR(8) DEFAULT NULL, player6 VARCHAR(8) DEFAULT NULL, player7 VARCHAR(8) DEFAULT NULL, player8 VARCHAR(8) DEFAULT NULL, player9 VARCHAR(8) DEFAULT NULL, player10 VARCHAR(8) DEFAULT NULL, player11 VARCHAR(8) DEFAULT NULL)')

def deleteTable1():
  c.execute("DROP TABLE IF EXISTS gameweekScores")

def deleteTable2():
  c.execute("DROP TABLE IF EXISTS gameweeks")

def deleteTable3():
  c.execute("DROP TABLE IF EXISTS gameweekSquads")


  
def dataEntry2():
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT matchDate FROM matchFixtures')
  ans = c.fetchall()
  finalFixtureDate = ans[-1][0]
  #print(finalFixtureDate)

  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  startDate = '2021-08-12'
  endDate = getDate(str(startDate))+timedelta(days=7)
  startID = 1
  while str(endDate) < finalFixtureDate:
    endDate = getDate(str(startDate))+timedelta(days=7)
    c.execute("INSERT INTO gameweeks (gameWeekID, windowStart, windowEnd) VALUES(?,?,?)",(startID,startDate,endDate))
    conn.commit()
    startID += 1
    startDate = endDate
  c.close()
  conn.close()

  

  

deleteTable1()
createTable1()
deleteTable2()
createTable2()
deleteTable3()
createTable3()
dataEntry2()

