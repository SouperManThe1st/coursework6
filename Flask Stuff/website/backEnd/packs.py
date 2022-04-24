
import sqlite3
import random
from website.backEnd.activeSquad import getClubPlayers
from flask import flash

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()
c.execute('SELECT IDnumber, name,currentPrice FROM playerStats ORDER BY currentPrice')
ans = c.fetchall()
c.close()
conn.close()

  
rarityDict = {'B':[10,5,2,1],'A':[2,2,2,1],'S':[1,2,3,8],'U':[1,5,10,10]} #Don't actually inlude U
def generatePlayerPool(ans,rarityDict,rarity):  #may have to generate different pools depending on level of pack
  playerPool = []
  for i in ans:
    if i[2] <= 40:
      for x in range(rarityDict[rarity][0]):
        playerPool.append((i[0],i[1]))
    elif i[2] >= 40 and i[2] <= 75:
      for x in range(rarityDict[rarity][1]):
        playerPool.append((i[0],i[1]))
    elif i[2] >= 75 and i[2] <= 105:
      for x in range(rarityDict[rarity][2]):
        playerPool.append((i[0],i[1]))
    else:
      for x in range(rarityDict[rarity][3]):
        playerPool.append((i[0],i[1]))
  return playerPool

def getPrice(playerID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT currentPrice FROM playerStats WHERE IDnumber = ?',(playerID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  return ans[0][0]

def generatePack(playerPool):
  pack = []
  packSize = 1
  while len(pack) < packSize:
    choice = random.randint(0,len(playerPool)-1) 
    if playerPool[choice] not in pack:
      pack.append(playerPool[choice][0])
  for player in pack:
    print(player)
  return pack
  

def getStarterPackPlayers(quality,playerArray,numPlayers):
  selected = []
  while len(selected) < numPlayers:
    choice = random.randint(0,3) 
    while quality[choice] == 0:
      choice = random.randint(0,3)
    if choice == 0:
      playerArray2 = playerArray[:len(playerArray)//4]
    elif choice == 1:
      playerArray2 = playerArray[len(playerArray)//4:len(playerArray)//2]
    elif choice == 2:
      playerArray2 = playerArray[len(playerArray)//2:round(len(playerArray)/(1.3))]
    elif choice == 3:
      playerArray2 = playerArray[round(len(playerArray)/(1.3)):]
    

    playerChoice = random.randint(0,len(playerArray2)-1)
    if playerArray2[playerChoice] not in selected:
      selected.append(playerArray2[playerChoice])
      quality[choice] -= 1
  
  return selected

def StarterPack(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  GKarray = []
  DFarray = []
  MFarray = []
  FWarray = []
  c.execute('SELECT IDnumber, name,currentPrice, position FROM playerStats ORDER BY currentPrice')
  ans = c.fetchall()
  c.close()
  conn.close
  for i in ans:
    if i[3] == 'GK':
      GKarray.append(i[0])
    elif i[3] == 'DF':
      DFarray.append(i[0])
    elif i[3] == 'MF':
      MFarray.append(i[0])
    elif i[3] == 'FW':
      FWarray.append(i[0])
  quality = [8,6,4,2]

  GKarray2 = getStarterPackPlayers(quality,GKarray,2)
  DFarray2 = getStarterPackPlayers(quality,DFarray,6)
  MFarray2 = getStarterPackPlayers(quality,MFarray,5)
  FWarray2 = getStarterPackPlayers(quality,FWarray,5)

  newPlayers = []
  for playerID in GKarray2:
    newPlayers.append(playerID)
  for playerID in DFarray2:
    newPlayers.append(playerID)
  for playerID in MFarray2:
    newPlayers.append(playerID)
  for playerID in FWarray2:
    newPlayers.append(playerID)
  newBalance = 1000
  return newBalance, newPlayers


  

  


    

    
  
  


  

  


def getTotalValue(pack):
  totalValue = 0
  for x in pack:
    totalValue += getPrice(x)
    #print(totalValue)
  return totalValue

def RarityTesting(numberOfTrials):
  arrB = []
  arrA = []
  arrS = []

  for x in range(numberOfTrials):
    arrB.append(getTotalValue(generatePack(generatePlayerPool(ans,rarityDict,'B'))))
    arrA.append(getTotalValue(generatePack(generatePlayerPool(ans,rarityDict,'A'))))
    arrS.append(getTotalValue(generatePack(generatePlayerPool(ans,rarityDict,'S'))))
  prices = []
  prices.append(round(sum(arrB)/numberOfTrials))
  prices.append(round(sum(arrA)/numberOfTrials))
  prices.append(round(sum(arrS)/numberOfTrials))
  return prices

#print(RarityTesting(500))
#pack = generatePack(generatePlayerPool(ans,rarityDict,'S'))
#print(pack)

def sellPlayer(playerID,clubID):
  currentBalance = getBalance(clubID)
  currentBalance += getPrice(playerID)
  print(currentBalance)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('UPDATE userClubs SET balance = ?',(currentBalance,))
  conn.commit()
  c.close()
  conn.close()

  
  
  

def keepPlayer(playerID,clubID):
  playersInClub = getClubPlayers(clubID)
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  if playerID not in playersInClub:
    c.execute("INSERT INTO clubsPlayers (clubID, playerID, priceWhenPacked) VALUES(?,?,?)",(clubID, playerID, getPrice(playerID)))
    conn.commit()
    c.close()
    conn.close()
  else:
    flash('This player was a duplicate and has been sold instead',category='error')
    sellPlayer(playerID,clubID)


def dealWithPack(pack):
  newPlayers = []
  newBalance = 0
  for x in pack:
    price = getPrice(x)  
    invalidChoice = True
    while invalidChoice == True:
      try:      
        choice = input(f"keep {x} or sell for {price} (k or s) ?\n").lower()
        if choice == 'k':
          newPlayers.append(x)
          invalidChoice = False
        elif choice == 's':
          newBalance += price
          invalidChoice = False
        else:
          print("Invalid Choice")
      except:
        print("Invalid Choice")
  return newBalance, newPlayers
  
def getNameFromID(playerID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT name FROM playerStats WHERE IDnumber = ?',(playerID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  return ans[0][0]


#clubID = 1
#newBalance, newPlayers = dealWithPack(pack)
#print(newBalance, newPlayers)

def getBalance(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT balance from userClubs WHERE clubID = ?',(clubID,))
  balanceAns = c.fetchall()
  c.close()
  conn.close()
  currentBalance = balanceAns[0][0]
  return currentBalance

def updateBalance(newBalance,clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'UPDATE userClubs SET balance = ? WHERE clubID = ?',(newBalance,clubID,))
  conn.commit()
  c.close()
  conn.close()

def updateDataBaseAfterPack(newBalance,newPlayers,clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT balance from userClubs WHERE clubID = ?',(clubID,))
  balanceAns = c.fetchall()
  currentBalance = balanceAns[0][0]
  currentBalance += newBalance
  c.execute(f'UPDATE userClubs SET balance = ? WHERE clubID = ?',(currentBalance,clubID,))
  conn.commit()
  c.close()
  conn.close()
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT playerID from clubsPlayers WHERE clubID = ?',(clubID,))
  playersInClubAns = c.fetchall()
  playersInClub = []
  for x in playersInClubAns:
    playersInClub.append(x[0])
  for playerID in newPlayers:
    if playerID in playersInClub:
      newBalance += getPrice(playerID)
      name = getNameFromID(playerID)
      print(f"{name} is a duplicate and will be sold instead")
      pass
    else:
      c.execute("INSERT INTO clubsPlayers (clubID, playerID, priceWhenPacked) VALUES(?,?,?)",(clubID, playerID, getPrice(playerID)))
  conn.commit()
  c.close()
  conn.close()

#updateDataBaseAfterPack(newBalance,newPlayers,clubID)


def getPackChoice(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT balance from userClubs WHERE clubID = ?',(clubID,))
  balanceAns = c.fetchall()
  currentBalance = balanceAns[0][0]
  print(f"Current Balance is {currentBalance}")

  basicCost = 600
  advancedCost = 1200
  supremeCost = 1800

  print(f'1: Basic ({basicCost})')
  print(f'2 : Advanced ({advancedCost})')
  print(f'3 : Supreme ({supremeCost})')
  print('4 : Exit pack store')


  invalidChoice = True
  while invalidChoice == True:
    try:
      choice = int(input("Enter choice of pack:\n"))
      if choice == 1:
        cost = basicCost
        rarity = 'B'
        invalidChoice = False
      elif choice == 2:
        cost = advancedCost
        rarity = 'A'
        invalidChoice = False
      elif choice == 3:
        cost = supremeCost
        rarity = 'S'
        invalidChoice = False
      elif choice == 4:
        return -1
      else:
        print("Invalid Choice")
    except:
      print("Invalid Choice")
  
  if choice != 4:
    if currentBalance < cost:
      print("You do not have enough coins to open this pack - returning to the store")
      rarity = getPackChoice(clubID)
    else:
      newBalance = currentBalance - cost
      c.execute(f'UPDATE userClubs SET balance = ? WHERE clubID = ?',(newBalance,clubID,))
      conn.commit()
      c.close()
      conn.close()

    return rarity
  else:
    return -1


def getBalance(clubID):
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute(f'SELECT balance FROM userClubs WHERE clubID = ?',(clubID,))
  ans = c.fetchall()
  c.close()
  conn.close()
  if len(ans) != 0:
    balance = ans[0][0]
    return balance
  else:
    return -1
    

def openPack(clubID,rarity):
  pack = generatePack(generatePlayerPool(ans,rarityDict,rarity))
  newBalance, newPlayers = dealWithPack(pack)
  updateDataBaseAfterPack(newBalance,newPlayers,clubID)



def openStarterPack(clubID):
  newBalance, newPlayers = StarterPack(clubID)
  updateDataBaseAfterPack(newBalance,newPlayers,clubID)



def packsMain(clubID):
  invalidChoice = True
  while invalidChoice == True:
    print("1: Open a pack")
    print("2 : Exit store page")
    try:
      choice = int(input("Enter choice: "))
      if choice == 1:
        rarity = getPackChoice(clubID)
        if rarity == -1:
          print("Exiting Pack Store")
          return False
        else:
          openPack(clubID,rarity)
        invalidChoice = False
        packsMain(clubID)
      elif choice == 2:
        print("You are now exiting the club screen")
        invalidChoice = False
      else:
        print("Invalid Choice\n")
    except:
      print("Invalid Choice")
  

#clubID = 3
#openStarterPack(clubID)
#packsMain(clubID)