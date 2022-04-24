from ast import Str
import sqlite3
from datetime import date, timedelta
from activeSquad import getUpcomingFixtures,setThisWeeksSquad,getCurrentGameweekID,setBalanceAfterGameweek
from userClub import getUsersClub

clubIDs = []
try:
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT clubID FROM userClubs')
  ans = c.fetchall()
  for i in ans:
    #print(i[0])
    clubIDs.append(i[0])
  currentGameweek = getCurrentGameweekID()
  for clubID in clubIDs:
      setThisWeeksSquad(clubID,currentGameweek)
      #setThisWeeksSquad(clubID,currentGameweek-1)
      setBalanceAfterGameweek(clubID,currentGameweek-1)
except:
  print("No existing database")




