from ast import Str
import sqlite3
from datetime import date, timedelta, datetime
import requests

def getBalance(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT balance from userClubs WHERE clubID = ?',(clubID,))
  balanceAns = c.fetchall()
  c.close()
  conn.close()
  currentBalance = balanceAns[0][0]
  return currentBalance


def orderByPosition(playerArray):
  FW = []
  MF = []
  DF = []
  GK = []
  ordered = []
  for playerID in playerArray:
    position = getPlayerPosition(playerID)
    if position == 'FW':
      FW.append(playerID)
    elif position == 'MF':
      MF.append(playerID)
    elif position == 'DF':
      DF.append(playerID)
    elif position == 'GK':
      GK.append(playerID)
  for playerID in GK:
    ordered.append(playerID)
  for playerID in DF:
    ordered.append(playerID)
  for playerID in MF:
    ordered.append(playerID)
  for playerID in FW:
    ordered.append(playerID)
  return ordered

    

def getPlayerPosition(playerID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT position from playerStats where IDnumber = ?',(playerID,))
  ans = c.fetchall()
  position = ans[0][0]
  return position


def getClubPlayers(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT playerID from clubsPlayers where clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  if ans == None:
    return 'No players In club'
  clubPlayers = []
  for i in ans:
    #print(i[0])
    clubPlayers.append(i[0])
  return clubPlayers


def removePlayerFromClub(clubID,playerID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'DELETE from clubsPlayers where clubID = ? and playerID = ?',(clubID,playerID,))
  conn.commit()
  c.close()
  conn.close()


def getPackPlayersDetails(Pack):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  clubPlayersInfo = []
  for playerID in Pack:
    playerInfo = []
    c.execute(f'SELECT name,position,team from playerStats where IDnumber = ?',(playerID,))
    ans = c.fetchall()
    name = ans[0][0]
    position = ans[0][1]
    team = ans[0][2]
    playerInfo.append(name)
    playerInfo.append(position)
    playerInfo.append(team)
    playerInfo.append(playerID)
    clubPlayersInfo.append(playerInfo)
  #for player in clubPlayersInfo:
    #print(player)
  c.close()
  conn.close()
  return clubPlayersInfo

def getClubPlayerDetails(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT IDnumber,name,position,team from playerStats INNER JOIN clubsPlayers ON playerStats.IDnumber = clubsPlayers.playerID WHERE clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  clubPlayersInfo = []
  for i in ans:
    playerInfo = []
    name = i[1]
    position = i[2]
    team = i[3]
    
    playerInfo.append(name)
    playerInfo.append(position)
    playerInfo.append(team)
    playerInfo.append(i[0])
    clubPlayersInfo.append(playerInfo)
  return clubPlayersInfo

  


def getPriceWhenPacked(playerID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT priceWhenPacked from clubsPlayers where playerID = ?',(playerID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  return ans[0]


#clubPlayers = getClubPlayers(clubID)
#getClubPlayersDetails(clubID)
#print(clubPlayers)
#yetToBeSelectedClubPlayers = clubPlayers

def addPlayer(slots,index,yetToBeSelectedClubPlayers):
  selectedPosition = slots[index]
  print(selectedPosition)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT IDnumber,name,team FROM playerStats WHERE position = ?',(selectedPosition,))
  ans = c.fetchall() #all players in that position
  c.close()
  conn.close()
  availablePlayers = []
  availablePlayersNames = []
  availablePlayersTeams = []
  if len(ans) == 0:
    return 'N/A'
  for i in ans:
    if i[0] in yetToBeSelectedClubPlayers:
      availablePlayers.append(i[0])
      availablePlayersNames.append(i[1])
      availablePlayersTeams.append(i[2])
  #print(availablePlayersNames)
  if len(availablePlayersNames) >0:
    invalidChoice = True
    while invalidChoice == True:
      for x in range(len(availablePlayersNames)):
        print(f'{x+1}:{availablePlayersNames[x]} ({availablePlayersTeams[x]})')
      try:
        playerToAddChoice = int(input("\nSelect Player \n"))-1
        print('')
        playerToAdd = availablePlayers[playerToAddChoice]
        yetToBeSelectedClubPlayers.remove(playerToAdd)
        invalidChoice = False
      except:
        print("Invalid Choice")
        print('')
  else:
    print("No available players\n")
    playerToAdd = slots[index]
  return playerToAdd,yetToBeSelectedClubPlayers

def addPlayerToSquad(playerID,index,clubID):
  index = int(index)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  playerColumns = ['player1','player2','player3','player4','player5','player6','player7','player8','player9','player10','player11']
  playerChoice = playerColumns[index]
  #c.execute("UPDATE clubsActiveSquads SET (?)=? WHERE clubID=?", (playerChoice, playerID, clubID,))
  c.execute(f'UPDATE clubsActiveSquads SET {playerChoice} = ? WHERE clubID = ?',(playerID,clubID,))
  conn.commit()
  c.close()
  conn.close()

def addPlayerToStarterSquad(slots,index,yetToBeSelectedClubPlayers):
  selectedPosition = slots[index]
  print(selectedPosition)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT IDnumber,name,team FROM playerStats WHERE position = ?',(selectedPosition,))
  ans = c.fetchall() #all players in that position
  c.close()
  conn.close()
  availablePlayers = []
  availablePlayersNames = []
  availablePlayersTeams = []
  if len(ans) == 0:
    return 'N/A'
  for i in ans:
    if i[0] in yetToBeSelectedClubPlayers:
      availablePlayers.append(i[0])
      availablePlayersNames.append(i[1])
      availablePlayersTeams.append(i[2])
  #print(availablePlayersNames)
  if len(availablePlayersNames) >0:
    invalidChoice = True
    while invalidChoice == True:
      for x in range(len(availablePlayersNames)):
        print(f'{x+1}:{availablePlayersNames[x]} ({availablePlayersTeams[x]})')
      try:
        playerToAddChoice = 1 ######### FOR STARTER SQUAD
        playerToAdd = availablePlayers[playerToAddChoice]
        print(playerToAdd)
        yetToBeSelectedClubPlayers.remove(playerToAdd)
        invalidChoice = False
      except:
        print("Invalid Choice")
        print('')
  else:
    print("No available players\n")
    playerToAdd = slots[index]
  return playerToAdd,yetToBeSelectedClubPlayers

def selectFormation():
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * from formations ')
  ans = c.fetchall() #### the different choices of formation
  c.close()
  conn.close()
  for i in ans:
    print(f'{i[0]} : {i[1:]}')
  print('')
  selectedFormation = int(input("Enter formation choice \n"))-1
  numGK = 1
  numDF = ans[selectedFormation][1]
  numMF = ans[selectedFormation][2]
  numFW = ans[selectedFormation][3]
  slots = []
  slots.append('GK')
  for x in range(numDF):
    slots.append('DF')
  for x in range(numMF):
    slots.append('MF')
  for x in range(numFW):
    slots.append('FW')
  print(slots)
  return slots

def getAllFormations():
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * from formations')
  ans = c.fetchall() #### the different choices of formation
  c.close()
  conn.close()
  arr = []
  for i in ans:
    arr.append(i)
  return arr

def updateFormation(clubID,formationID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('UPDATE clubsActiveSquads SET formationID = ? where clubID = ?',(formationID,clubID,))
  conn.commit()
  c.close()
  conn.close()

def getCurrentFormationID(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT formationID from clubsActiveSquads where clubID = ?',(clubID,))
  ans = c.fetchall() 
  c.close()
  conn.close()
  print(ans[0][0])
  return ans[0][0]

def getFormationName(formationID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT DF,MF,FW from formations where formationID = ?',(formationID,))
  ans = c.fetchall()[0] 
  c.close()
  conn.close()
  return f'{ans[0]}-{ans[1]}-{ans[2]}'

def getFormationStructure(formationID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * from formations where formationID = ?',(formationID,))
  ans = c.fetchall() #### the different choices of formation
  c.close()
  conn.close()
  structure = ['GK']
  numDF = ans[0][1]
  numMF = ans[0][2]
  numFW = ans[0][3]
  for i in range(numDF):
    structure.append('DF')
  for j in range(numMF):
    structure.append('MF')
  for k in range(numFW):
    structure.append('FW')
  return structure


def createSquad(yetToBeSelectedClubPlayers,clubID):
  if len(yetToBeSelectedClubPlayers) == 0:
    print('No players in club')
  else:
    slots = selectFormation()
    for index in range(len(slots)):
      player, yetToBeSelectedClubPlayers = addPlayer(slots,index,yetToBeSelectedClubPlayers)
      slots[index] = player
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    for playerIDnumber in slots:
      try:
        c.execute(f'SELECT name,team FROM playerStats WHERE IDnumber = ?',(playerIDnumber))
        ans = c.fetchall()
        c.close()
        conn.close()
        print(f'{ans[0][0]} ({ans[0][1]}) ')
      except:
        print(playerIDnumber)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute("UPDATE clubsActiveSquads SET player1 = ?, player2 = ?, player3 = ?, player4 = ?, player5 = ?, player6 = ?, player7 = ?, player8 = ?, player9 = ?, player10 = ?, player11 = ? WHERE clubID = ?",(slots[0],slots[1],slots[2],slots[3],slots[4],slots[5],slots[6],slots[7],slots[8],slots[9],slots[10],clubID))
    conn.commit()
    c.close()
    conn.close()
    #clubPlayers = getClubPlayers(clubID)
    #getClubPlayersDetails(clubPlayers)
    #print(clubPlayers)
    #yetToBeSelectedClubPlayers = clubPlayers
    return slots

  
def makeStarterSquad(clubID,formationID):
    clubPlayers = getClubPlayers(clubID)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM clubsActiveSquads WHERE clubID = ?',(clubID,))
    ans = c.fetchall()
    c.close()
    conn.close()
    players = ans[0][2:13]
    print(players)
    used = []

    positions = ['GK','DF','DF','DF','DF','MF','MF','MF','FW','FW','FW']
    positions = getFormationStructure(formationID)
    for player in players:
        used.append(player)
    count = 0
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    for x in players:
        if x in clubPlayers:
            print('already in squad')
        else:
            position = positions[count]
            player = getFirstAvailablePlayer(position,clubID,used)
            print(player)
            used.append(player)
            count+=1
    slots = players
    c.execute("UPDATE clubsActiveSquads SET player1 = ?, player2 = ?, player3 = ?, player4 = ?, player5 = ?, player6 = ?, player7 = ?, player8 = ?, player9 = ?, player10 = ?, player11 = ? WHERE clubID = ?",(slots[0],slots[1],slots[2],slots[3],slots[4],slots[5],slots[6],slots[7],slots[8],slots[9],slots[10],clubID))
    conn.commit()
    c.close()
    conn.close()


def createStarterSquad(yetToBeSelectedClubPlayers,clubID,formationID):
  if len(yetToBeSelectedClubPlayers) == 0:
    print('No players in club')
  else:
    used = []
    #slots  = ['GK','DF','DF','DF','DF','MF','MF','MF','FW','FW','FW']
    slots = getFormationStructure(formationID)
    for index in range(len(slots)):
      player, yetToBeSelectedClubPlayers = addPlayerToStarterSquad(slots,index,yetToBeSelectedClubPlayers)
      if player in slots:
        formation = slots
        position = slots[index]
        player = getFirstAvailablePlayer(position,clubID,used)
      slots[index] = player
      used.append(player)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    for playerIDnumber in slots:
      try:
        c.execute(f'SELECT name,team FROM playerStats WHERE IDnumber = ?',(playerIDnumber))
        ans = c.fetchall()
        c.close()
        conn.close()
        print(f'{ans[0][0]} ({ans[0][1]}) ')
      except:
        print(playerIDnumber)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute("UPDATE clubsActiveSquads SET player1 = ?, player2 = ?, player3 = ?, player4 = ?, player5 = ?, player6 = ?, player7 = ?, player8 = ?, player9 = ?, player10 = ?, player11 = ? WHERE clubID = ?",(slots[0],slots[1],slots[2],slots[3],slots[4],slots[5],slots[6],slots[7],slots[8],slots[9],slots[10],clubID))
    conn.commit()
    c.close()
    conn.close()
    #clubPlayers = getClubPlayers(clubID)
    #getClubPlayersDetails(clubPlayers)
    #print(clubPlayers)
    #yetToBeSelectedClubPlayers = clubPlayers
    return slots


def getFirstAvailablePlayer(position,clubID,used):
  #clubPlayers = getClubPlayers(clubID)
  clubPlayersDetails = getClubPlayerDetails(clubID)
  for player in clubPlayersDetails:
    if player[1] == position:
      if player[-1] not in used:
        #print(player[-1])
        return player[-1]

  
  


def ViewMySquad(clubID):
  #clubsPlayers = getClubPlayers(clubID)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * FROM clubsActiveSquads WHERE clubID = ?',(clubID,))
  ans = c.fetchall()
  formation = ans[0][1]
  players = ans[0][2:]
  print(formation)
  print(players)
  squad = []
  ans = c.execute('SELECT DF,MF,FW FROM formations WHERE formationID = ?',(formation,))
  ans = c.fetchall()[0]
  print(ans)
  for i in range(11):
    playerID = players[i]
    print(playerID)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    playerInfo = []
    c.execute(f'SELECT name,position,team from playerStats where IDnumber = ?',(playerID,))
    ans2 = c.fetchall()
    c.close()
    conn.close()
    name = ans2[0][0]
    position = ans2[0][1]
    team = ans2[0][2]
    playerInfo.append(position)
    playerInfo.append(name)
    playerInfo.append(team)
    playerInfo.append(playerID)
    squad.append(playerInfo)
  print(squad)
  return squad

def viewSquad(clubID):
  clubPlayers = getClubPlayers(clubID)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * FROM clubsActiveSquads WHERE clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  print(ans[0][2:13])
  formation = ans[0][1]
  options = ['player1','player2','player3','player4','player5','player6','player7','player8','player9','player10','player11']
  squad = []
  used = []
  for i in range(2,13):
    playerID = ans[0][i]

    #if playerID in clubPlayers:
    if playerID in clubPlayers:
      print('HEHEHE')
    used.append(playerID)
    print('yes')
    print(playerID)
    if playerID not in clubPlayers:
      position = getFormationStructure(formation)[i-2]
      playerID = getFirstAvailablePlayer(position,clubID,used)
      used.append(playerID)
      #playerID = 'Pick A Player'
      #playerID = "bc7dc64d"
    print(clubPlayers)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    try:
      playerInfo = []
      c.execute('SELECT name,position,team from playerStats where IDnumber = ?',(playerID,))
      ans2 = c.fetchall()
      c.close()
      conn.close()
      name = ans2[0][0]
      position = ans2[0][1]
      team = ans2[0][2]
      playerInfo.append(position)
      playerInfo.append(name)
      playerInfo.append(team)
      playerInfo.append(playerID)
      squad.append(playerInfo)
      print(f'{name} ({team})')
    except:
      print(playerID)
  print(squad)
  return squad

  

def getCurrentGameweekID():
  todaysDate = datetime.today().strftime('%Y-%m-%d')
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT gameweekID FROM gameweeks where windowEnd > ?',(todaysDate,))
  ans = c.fetchall()
  currentGameweekID = ans[0][0]
  return currentGameweekID

def IsPlayerTeamActive(playerID):
  gameweekID = getCurrentGameweekID()+1
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT IDnumber,matchDate FROM playerStats,matchFixtures,gameweeks WHERE ((playerStats.team = matchFixtures.homeTeam) OR (playerStats.team = matchFixtures.awayTeam)) AND (playerStats.IDnumber = ?) AND (matchFixtures.matchDate between gameweeks.windowStart and gameweeks.windowEnd) AND (gameweeks.gameweekID = ?) ORDER BY matchFixtures.matchDate DESC',(playerID,gameweekID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  print(ans)
  if len(ans) > 0:
    return True
  else:
    return False


  






def getAllGameweeks(clubID):
  lastGameweek = getCurrentGameweekID()-1
  gameweeks = {}
  for week in range(1,lastGameweek+1):
    gameweeks[week] = 'N/A'
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT gameweekID,weekScore FROM gameweekScores where clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  #print(ans)
  for i in ans:
    try:
      gameweeks[i[0]] = i[1]
    except:
      pass
  return gameweeks




def getPlayerPoints(IDnumber,gameweekID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT windowStart,windowEnd FROM gameweeks WHERE gameweekID = ?',(gameweekID,))
  ans = c.fetchall()
  #print(ans)
  windowStart = ans[0][0]
  windowEnd = ans[0][1]
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT matchPoints FROM playerMatches where IDnumber = ? AND matchDates between ? and ?',(IDnumber,windowStart,windowEnd,))
  ans = c.fetchall()
  arr = []
  for i in ans:
    arr.append(i[0])
  return sum(arr)


IDnumber = 'bc7dc64d'
gameweekID = 10
windowStart = '2021-10-30'
windowEnd = '2021-12-01'
#print(getPlayerPoints(IDnumber,gameweekID))

#run this script every Thursday    
def getSquadPoints(clubID,gameweekID):
  try:
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute('SELECT * FROM gameweekSquads WHERE clubID = ? and gameweekID = ?',(clubID,gameweekID,))
    ans = c.fetchall()
    c.close()
    conn.close()
    squad = ans[-1][2:]
    print(squad)
    total = 0
    arr = []
    for playerID in squad:
      total += getPlayerPoints(playerID,gameweekID)
      arr.append(getPlayerPoints(playerID,gameweekID))
    print(arr)
    print(f"length = {len(arr)}")
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute("INSERT INTO gameweekScores (gameweekID, clubID, weekScore) VALUES(?,?,?)",(gameweekID,clubID,total))
    conn.commit()
    c.close()
    conn.close()
    return total
  except:
    return 'N/A'

def setBalanceAfterGameweek(clubID,gameweekID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  try:
    c.execute('SELECT weekScore FROM gameweekScores WHERE clubID = ? and gameweekID = ?',(clubID,gameweekID))
    ans = c.fetchall()
    score = ans[0][0]
  except:
    score = 0
  c.execute('UPDATE userClubs SET balance = balance + ?',(score,))
  conn.commit()
  c.close()
  conn.close()



def setThisWeeksSquad(clubID,currentGameweekID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * FROM clubsActiveSquads WHERE clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  squad = ans[0][2:]
  #print(squad)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute("INSERT INTO gameweekSquads (gameweekID, clubID, player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(currentGameweekID,clubID,squad[0],squad[1],squad[2],squad[3],squad[4],squad[5],squad[6],squad[7],squad[8],squad[9],squad[10],))
  conn.commit()
  c.close()
  conn.close()

#setThisWeeksSquad(14,31)
#getSquadPoints(14,31)

def retrieveSquadPoints(clubID,gameweekID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT weekScore from gameweekScores WHERE clubID = ? AND gameweekID = ? ORDER BY gameweekID ASC',(clubID,gameweekID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  #return ans
  try:
    return ans[-1][0]
  except:
    return 'N/A'

#print(retrieveSquadPoints(14,31))


def getUpcomingFixtures():
  today =str(datetime.today())[0:10]
  print(today)
  endDate = str((datetime.today())+timedelta(days=7))[0:10]
  print(endDate)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * FROM matchFixtures WHERE matchDate between ? and ?',(today,endDate,))
  ans = c.fetchall()
  if len(ans) == 0:
    ans.append('No upcoming fixtures in the next week')
  return ans

#getUpcomingFixtures()
  

