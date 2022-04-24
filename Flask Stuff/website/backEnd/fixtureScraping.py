import requests
import re
from datetime import date
import sqlite3


def getDate(d1):
  d1 = date(int(d1[0:4]),int(d1[5:7]),int(d1[8:10]))
  return d1

fixtures_Url = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'

request = requests.get(fixtures_Url)
page = request.text
tableStart = page.index('<tbody')
tableEnd = page.index('</tbody>')
match_table = page[tableStart:tableEnd]
RowStarts = [i for i in range(len(match_table)) if match_table.startswith('<tr', i)]
RowEnds = [i for i in range(len(match_table)) if match_table.startswith('</tr>', i)]

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()

def createTable1(): #Results
  c.execute('CREATE TABLE IF NOT EXISTS matchResults (matchDate DATE (12), matchTime VARCHAR (8), homeTeam VARCHAR (50), awayTeam VARCHAR (50), matchScore VARCHAR (5))')

def createTable2(): #Fixtures
  c.execute('CREATE TABLE IF NOT EXISTS matchFixtures (matchDate DATE (12), matchTime VARCHAR, homeTeam VARCHAR (50), awayTeam VARCHAR (50))')

def deleteTable1():
  c.execute("DROP TABLE IF EXISTS matchResults")

def deleteTable2():
  c.execute("DROP TABLE IF EXISTS matchFixtures")

deleteTable1()
createTable1()
deleteTable2()
createTable2()

def dataEntry1(matchDate,matchTime,homeTeam,awayTeam,matchScore): #AddResult
  c.execute("INSERT INTO matchResults (matchDate, matchTime, homeTeam, awayTeam, matchScore) VALUES(?,?,?,?,?)",(matchDate,matchTime,homeTeam,awayTeam,matchScore))
  conn.commit()

def dataEntry2(matchDate,matchTime,homeTeam,awayTeam): #AddFixture
  c.execute("INSERT INTO matchFixtures (matchDate, matchTime, homeTeam, awayTeam) VALUES(?,?,?,?)",(matchDate,matchTime,homeTeam,awayTeam))
  conn.commit()

for z in range(len(RowStarts)):
  current = match_table[RowStarts[z]:RowEnds[z]:]
  matchDate = current[current.find('data-stat="date"')+22:current.find('data-stat="date"')+30]
  #matchDate = getDate(matchDate)
  matchDate = matchDate[0:4] + '-' + matchDate[4:6] + '-' + matchDate[6:8]
  print(matchDate)

  matchTime = current[current.find('data-stat="time"')+22:current.find('data-stat="time"')+30]

  print(matchTime)

  add = current.find('/en/squads')
  homeTeamStart = current[current.find('/en/squads'):].find('">') + add + 2
  homeTeamEnd = current[current.find('/en/squads'):].find('</a>') + add
  homeTeam = current[homeTeamStart:homeTeamEnd]
  print(homeTeam)

  add = current.rfind('/en/squads')
  awayTeamStart = current[current.rfind('/en/squads'):].find('">') + add + 2
  awayTeamEnd = current[current.rfind('/en/squads'):].find('</a>') + add
  awayTeam = current[awayTeamStart:awayTeamEnd]
  print(awayTeam)


  scoreLine = current[current.find('data-stat="score"'):]
  matchScore = scoreLine[scoreLine.find('">')+2:scoreLine.find('</a>')].replace('&ndash;','-')
  print(matchScore)

  if 'Match Postponed' not in current:
    if matchDate != '><td- c-la':
      if matchScore[0] in list('0123456789') and matchScore[-1] in list('0123456789'):
        dataEntry1(matchDate,matchTime,homeTeam,awayTeam,matchScore)
      else:
        dataEntry2(matchDate,matchTime,homeTeam,awayTeam)
  

