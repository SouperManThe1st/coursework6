import sqlite3


def createClub(userID): #DataEntry  
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    try:
      c.execute('SELECT clubID FROM userClubs ORDER BY clubID')
      ans = c.fetchall()
      clubID = ans[-1][0] + 1
    except:
      clubID = 1
    season = '21/22'
    #clubname = input("Enter club name\n")
    balance = 5000
    #clubPlayers = ''
    c.execute("INSERT INTO userClubs (userID,clubID,season, balance) VALUES(?,?,?,?)",(userID,clubID,season, balance))
    c.execute("INSERT INTO clubsActiveSquads (clubID,formationID) VALUES (?,?)",(clubID,1))
    conn.commit()
    c.close()
    conn.close()

#createClub()

def addClubMain(userID):
  createClub(userID)