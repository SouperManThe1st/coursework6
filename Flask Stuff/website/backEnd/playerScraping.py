import requests
import re
from datetime import date

def getDate(d1):
  d1 = date(int(d1[0:4]),int(d1[5:7]),int(d1[8:10]))
  return d1

playerAdvStats_Url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'


class Player:
  def __init__(self,IDnumber,name,nation,position,team,age,appearances,starts,minutes,goals,assists,penaltiesScored,penaltiesAttempted,yellowCards,redCards,minsPerGoal,minsPerAssist):
    currentCompetitionCode = 's11160'
    self.IDnumber = IDnumber
    self.name = name
    self.nation = nation
    self.position = position
    self.team = team
    self.age = age
    self.appearances = appearances
    self.starts = starts
    self.minutes = minutes
    self.goals = goals
    self.assists = assists
    self.penaltiesScored = penaltiesScored
    self.penaltiesAttempted = penaltiesAttempted
    self.yellowCards = yellowCards
    self.redCards = redCards
    self.minsPerGoal = minsPerGoal
    self.minsPerAssist =  minsPerAssist
    self.ProfileLink = f'https://fbref.com/en/players/{self.IDnumber}/'
    self.CurrentSeasonLink = f'https://fbref.com/en/players/{self.IDnumber}/matchlogs/{currentCompetitionCode}/summary/'
    self.GKlink = None
    if self.position == 'GK':
      GKlink = self.CurrentSeasonLink.replace('summary','keeper')
      self.GKlink = GKlink
    self.matchDates,self.matchWeeks,self.matchPoints = self.calculateMatchPoints()
    self.basePrice = self.calculateBasePrice()
    try:
      averageScore = sum(self.matchPoints) / len(self.matchPoints)
      change = (averageScore - self.basePrice) / 2
    except:
      change = 0
    #print(change)
    currentPrice = round(self.basePrice + change)
    self.currentPrice = currentPrice

  def getCurrentClub(self):
    '''
    gets the current club of the player.
    This means only players who currently play in the premier league are available in the game.
    '''
    request = requests.get(self.ProfileLink)
    page = request.text
    reversePage = page[::-1]
    tableStart = reversePage.index('<tbody>'[::-1])
    tableEnd = reversePage.index('</tbody>'[::-1])
    match_table = reversePage[tableEnd:tableStart][::-1]
    RowStarts = [i for i in range(len(match_table)) if match_table.startswith('<tr', i)]
    RowEnds = [i for i in range(len(match_table)) if match_table.startswith('</tr>', i)]
    lastRow = match_table[RowStarts[-1]:RowEnds[-1]]
    currentClubLine = lastRow[lastRow.find('en/squads'):]
    currentClub = currentClubLine[currentClubLine.find('">')+2:currentClubLine.find('</a>')]
    return currentClub
  
  
  
  def calculateMatchPoints(self):
    try:
      request = requests.get(self.CurrentSeasonLink)
      page = request.text
      tableStart = page.index('<tbody')
      tableEnd = page.index('</tbody>')
      match_table = page[tableStart:tableEnd]
      RowStarts = [i for i in range(len(match_table)) if match_table.startswith('<tr', i)]
      RowEnds = [i for i in range(len(match_table)) if match_table.startswith('</tr>', i)]
      match_list = []
      pointsArray = []
      datesArray = []
      matchWeeksArray = []

      for x in range(len(RowStarts)):
        current = match_table[RowStarts[x]:RowEnds[x]:]
        if ('class="unused_sub hidden"' not in current) and ('class="spacer partial_table"' not in current) and ('class="over_header thead"' not in current) and ('class="thead"') not in current:
          match_list.append(current)
      
      for match in match_list:

        dateStarts = [i for i in range(len(match)) if match.startswith('" >', i)]
        dateEnds = [i for i in range(len(match)) if match.startswith('</a>', i)]
        matchDate = match[match.index('">')+2:dateEnds[0]]
        datesArray.append(getDate(matchDate))
        
        tdEnds = [i for i in range(len(match)) if match.startswith('</td>', i)]
        
        matchWeekStart = match.index('Matchweek')
        matchWeek = match[matchWeekStart:dateEnds[1]]
        matchWeeksArray.append(matchWeek)
        
        position = match[dateStarts[8]+3:tdEnds[7]][:2]
        try:
          pos = position[-1] #W(forward), M(midfielder), B(defender), K(Goalkeeper)
        except:
          pos = 'M'

        minutes = int(match[dateStarts[9]+3:tdEnds[8]])

        minutesPoints = minutes / 90
        
        goals = int(match[dateStarts[10]+3:tdEnds[9]])
        goalsPoints = goals * 5
        if pos == 'M':
          goalsPoints *= 1.25
        if pos == 'D':
          goalsPoints *= 1.5
        if pos == 'G':
          goalsPoints *= 2
        

        assists = int(match[dateStarts[11]+3:tdEnds[10]])
        assistsPoints = assists * 4

        yellowCards = int(match[dateStarts[16]+3:tdEnds[15]])
        yellowCardsPoints = yellowCards * -1
        
        redCards = int(match[dateStarts[17]+3:tdEnds[16]])
        redCardsPoints = redCards * -3
        
        tackles = int(match[dateStarts[20]+3:tdEnds[19]])
        tacklesPoints = tackles * 0.1
        
        interceptions = int(match[dateStarts[21]+3:tdEnds[20]])
        interceptionsPoints = interceptions * 0.1

        blocks = int(match[dateStarts[22]+3:tdEnds[21]])
        blocksPoints = blocks * 0.1

        xG = float(match[dateStarts[23]+3:tdEnds[22]]) #ExpectedGoals
        xGPoints = (goals-xG)*2.5
        
        xA = float(match[dateStarts[25]+3:tdEnds[24]]) #ExpectedAssists
        xAPoints = (xA-assists)*2.5

        sca = int(match[dateStarts[26]+3:tdEnds[25]])#ShotCreatingActions
        scaPoints = sca * 0.25

        gca =int(match[dateStarts[27]+3:tdEnds[26]])#GoalCreatingActions
        gcaPoints = gca * 2.5

        passesMade = int(match[dateStarts[28]+3:tdEnds[27]])
        passesMadePoints = passesMade * 0.1

        progPasses = int(match[dateStarts[31]+3:tdEnds[30]])
        progPassesPoints = progPasses * 0.05

        progCarries = int(match[dateStarts[33]+3:tdEnds[32]])
        progCarriesPoints = progCarries * 0.35

        dribblesMade = int(match[dateStarts[34]+3:tdEnds[33]])
        dribblesMadePoints = dribblesMade * 0.05

        dribblesAtt = int(match[dateStarts[35]+3:tdEnds[34]])
        dribblesAtPoints = (dribblesMade-dribblesAtt) * 0.03

        outfieldPoints = float(minutesPoints + goalsPoints + assistsPoints + yellowCardsPoints + redCardsPoints + tacklesPoints + interceptionsPoints + interceptionsPoints + blocksPoints + xGPoints + xAPoints + scaPoints + gcaPoints + passesMadePoints + progPassesPoints + progCarriesPoints + dribblesMadePoints + dribblesAtPoints)

        outfieldPoints = int(round(outfieldPoints,1)*10)
        gkPoints = 0
      
        if position == 'GK':
          request = requests.get(self.GKlink)
          page = request.text
          tableStart = page.index('<tbody')
          tableEnd = page.index('</tbody>')
          match_table = page[tableStart:tableEnd]
          RowStarts = [i for i in range(len(match_table)) if match_table.startswith('<tr', i)]
          RowEnds = [i for i in range(len(match_table)) if match_table.startswith('</tr>', i)]
          match_list = []
          for x in range(len(RowStarts)):
            current = match_table[RowStarts[x]:RowEnds[x]:]
            if ('class="unused_sub hidden"' not in current) and ('class="spacer partial_table"' not in current) and ('class="over_header thead"' not in current) and ('class="thead"') not in current:
              match_list.append(current)
          for match in match_list:
            tdEnds = [i for i in range(len(match)) if match.startswith('</td>', i)]
            
            goalsAgainst = int(match[match.index('goals_against_gk')+19:tdEnds[10]])
            goalsAgainstPoints = goalsAgainst * - 1
            
            saves = int(match[match.index('saves')+8:tdEnds[11]])
            savePoints = saves * 2
            
            cleanSheets = int(match[match.index('clean_sheets')+15:tdEnds[13]])
            cleanSheetsPoints = cleanSheets * 5
            
            PSxG = float(match[match.index('psxg_gk')+10:tdEnds[14]])
            PSxGPoints = (PSxG-goalsAgainst) * 4

            gkPoints = goalsAgainstPoints + savePoints + cleanSheetsPoints + PSxGPoints 

            gkPoints = int(round(gkPoints,1)*5)            

        totalPoints = outfieldPoints+gkPoints

        #self.currentPrice += totalPoints/100
        pointsArray.append(totalPoints)
        
        
      #return matchweekPoints_list
      print(self.IDnumber)
      return datesArray,matchWeeksArray,pointsArray
    except:
      return [],[],[]
  
  def calculateBasePrice(self):
    '''
    This calculates the base price of a player based on how they performed in the previous season.
    '''
    try:
      request = requests.get(self.ProfileLink)
      page = request.text
      reversePage = page[::-1]
      tableStart = reversePage.index('<tbody>'[::-1])
      tableEnd = reversePage.index('</tbody>'[::-1])
      match_table = reversePage[tableEnd:tableStart][::-1]
      RowStarts = [i for i in range(len(match_table)) if match_table.startswith('<tr', i)]
      RowEnds = [i for i in range(len(match_table)) if match_table.startswith('</tr>', i)]
      for x in range(len(RowStarts)):
        current = match_table[RowStarts[x]:RowEnds[x]]
        if '2020-2021' in current:
          lastSeasonRow = current

      tdStarts = [i for i in range(len(lastSeasonRow)) if lastSeasonRow.startswith('<td', i)]
      tdEnds = [i for i in range(len(lastSeasonRow)) if lastSeasonRow.startswith('</td>', i)]
      tdStarts2 = [i for i in range(len(lastSeasonRow)) if lastSeasonRow.startswith('" >', i)]
      leagueLine = lastSeasonRow[tdStarts[3]:tdEnds[3]]
      leagueCountryLine = lastSeasonRow[tdStarts[2]:tdEnds[2]]
      country = leagueCountryLine[leagueCountryLine.rfind('">')+2:leagueCountryLine.rfind("</a>")]
      compLevel = leagueLine[leagueLine.find('">')+2:leagueLine.find("</span")-1]
      topCountries = ['ENG','FRA','GER','ESP','ITA']
      minutes = int(lastSeasonRow[tdStarts2[7]+3:tdEnds[5]].replace(',',''))
      minutesPoints = minutes / 90
      
      if self.position != 'GK':
        goals = int(lastSeasonRow[tdStarts2[8]+3:tdEnds[6]])
        goalsPoints = goals * 5
        if self.position == 'MF':
          goalsPoints *= 1.25
        if self.position == 'DF':
          goalsPoints *= 1.5
        
        assists = int(lastSeasonRow[tdStarts2[9]+3:tdEnds[7]])
        assistsPoints = assists * 4

        totalPoints = round(minutesPoints + goalsPoints + assistsPoints)
      
      else:
        goalsAgainst = int(lastSeasonRow[tdStarts2[8]+3:tdEnds[6]])
        if goalsAgainst == 0:
          goalsAgainst == 0.1

        concededPerGame = round((goalsAgainst / (minutes)) * 90,2)
        #print(concededPerGame)
        concededPerGamePoints = 100 - (concededPerGame * 38)

        totalPoints = round(minutesPoints + concededPerGamePoints)

      if compLevel != '1' and compLevel != 'Jr':
        multiplier = 0.6 / int(compLevel)
        totalPoints = round(totalPoints * multiplier)
      elif compLevel == 'Jr':
        totalPoints = 15

      if country not in topCountries:
        totalPoints = round(totalPoints * 0.6)

    except:
      totalPoints = 15
    
    totalPoints = round(totalPoints * 0.8)
    
    return totalPoints


def createPlayerObjectList(playerAdvStats_Url):
  '''
  Creates a list of all player objects.
  '''
  request = requests.get(playerAdvStats_Url) 
  r1 = re.finditer("<table", request.text) 
  arr = []
  for m in r1:
    span = []
    span.append(m.start())
    span.append(m.end())
    arr.append(span)
  player_table = request.text[arr[2][0]:]

  RowStarts = [i for i in range(len(player_table)) if player_table.startswith('<tr', i)]
  RowEnds = [i for i in range(len(player_table)) if player_table.startswith('</tr>', i)]

  player_list = []

  for x in range(2,len(RowStarts)):
    current = player_table[RowStarts[x]:RowEnds[x]:]
    if 'class="thead"' not in current:
      player_list.append(current)

  player_objects_list = []
  for player in player_list:
    IDnumber = re.search(r'players[\S](.{8})[\S]',player).group(1)
    name = re.search(r'data-stat="player" csk=".*?">(.*?)<',player).group(1)
    nation = re.search(r'data.*?country(.*?)-Football',player).group(1)[1:]
    position = re.search(r'data-stat="position".*?>(\w{2})',player).group(1)
    team = re.search(r'data-stat="squad".*?">(.*?)<',player).group(1)
    age = re.search(r'data-stat="age".*?>(\d{2})-',player).group(1)
    age = int(age)
    appearances = re.search(r'data-stat="games" >(\d+)<',player).group(1)
    appearances = int(appearances)
    starts = re.search(r'data-stat="games_starts" >(\d+)<',player).group(1)
    starts = int(starts)
    minutes = re.search(r'data-stat="minutes" csk="(\d+)"',player).group(1)
    minutes = int(minutes)
    goals = re.search(r'data-stat="goals" >(\d+)<',player).group(1)
    goals = int(goals)
    assists = re.search(r'data-stat="assists" >(\d+)<',player).group(1)
    assists = int(assists)
    penaltiesScored = re.search(r'data-stat="pens_made" >(\d+)<',player).group(1)
    penaltiesScored = int(penaltiesScored)
    penaltiesAttempted = re.search(r'data-stat="pens_att" >(\d+)<',player).group(1)
    penaltiesAttempted = int(penaltiesAttempted)
    yellowCards = re.search(r'data-stat="cards_yellow" >(\d+)<',player).group(1)
    yellowCards = int(yellowCards)
    redCards = re.search(r'data-stat="cards_red" >(\d+)<',player).group(1)
    redCards = int(redCards)
    if goals != 0:
      minsPerGoal = round(minutes/goals)
    else:
      minsPerGoal = 0
    if assists != 0:
      minsPerAssist = round(minutes/assists)
    else:
      minsPerAssist = 0
    
    playerObject = Player(IDnumber,name,nation,position,team,age,appearances,starts,minutes,goals,assists,penaltiesScored,penaltiesAttempted,yellowCards,redCards,minsPerGoal,minsPerAssist)

    player_objects_list.append(playerObject)
  return player_objects_list

player_objects_list = createPlayerObjectList(playerAdvStats_Url)


print("Starting DB creation")#No purpose - just here to indicate when the scraping has finished.

import sqlite3

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS playerStats (IDnumber VARCHAR(8), name VARCHAR(100), nation VARCHAR(100), position VARCHAR(2), team VARCHAR(50), age INT(2), appearances INT(2), starts INT(2), minutes INT(4), goals INT(2), assists INT(2), penaltiesScored INT(2), penaltiesAttempted INT(2), yellowCards INT(2), redCards INT(2), minsPerGoal INT DEFAULT NULL, minsPerAssist INT DEFAULT NULL, ProfileLink VARCHAR(200), CurrentSeasonLink VARCHAR(200), basePrice INT(3), currentPrice INT(3))')

def create_table2():
  c.execute('CREATE TABLE IF NOT EXISTS playerMatches (IDnumber VARCHAR(8), matchDates DATE (12), matchWeeks INT(2),matchPoints INT (3))')

def data_entry(player):
    '''
    Inserts the players details into a database that stores the players general information and statistics. 
    A player object's attributes correspond to the columns of the databse.
    '''
    IDnumber = player.IDnumber
    name = player.name
    nation = player.nation
    position = player.position
    team = player.team
    age = player.age
    appearances = player.appearances
    starts = player.starts
    minutes = player.minutes
    goals = player.goals
    assists = player.assists
    penaltiesScored = player.penaltiesScored
    penaltiesAttempted = player.penaltiesAttempted
    yellowCards = player.yellowCards
    redCards = player.redCards
    minsPerGoal = player.minsPerGoal
    minsPerAssist = player.minsPerAssist
    ProfileLink = player.ProfileLink
    CurrentSeasonLink = player.CurrentSeasonLink
    basePrice = player.basePrice
    currentPrice = player.currentPrice

    c.execute("INSERT INTO playerStats (IDnumber, name, nation, position, team, age, appearances, starts, minutes, goals, assists, penaltiesScored, penaltiesAttempted, yellowCards, redCards, minsPerGoal, minsPerAssist, ProfileLink, CurrentSeasonLink, basePrice, currentPrice) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",(IDnumber, name, nation, position, team, age, appearances, starts, minutes, goals, assists, penaltiesScored, penaltiesAttempted, yellowCards, redCards, minsPerGoal, minsPerAssist, ProfileLink, CurrentSeasonLink, basePrice, currentPrice))# ProfileLink, CurrentSeasonLink, matchPoints)) 
    conn.commit()

def data_entry2(player):
  '''
  Inserts the players match scores into the database that stores the points a player has scored throughout the season so far.
  '''
  IDnumber = player.IDnumber
  matchDates = player.matchDates
  matchWeeks = player.matchWeeks
  matchPoints = player.matchPoints
  for x in range(len(matchPoints)):
    c.execute("INSERT INTO playerMatches (IDnumber, matchDates, matchWeeks, matchPoints) VALUES(?,?,?,?)",(IDnumber,matchDates[x],matchWeeks[x],matchPoints[x]))
  conn.commit()

def delete_table():
  c.execute("DROP TABLE IF EXISTS playerStats")

def delete_table2():
  c.execute("DROP TABLE IF EXISTS playerMatches")
  

delete_table()
create_table()
delete_table2()
create_table2()
for player in player_objects_list:
  if player.getCurrentClub() == player.team and len(player.matchDates) != 0:
    data_entry(player)
    data_entry2(player)
 
c.close()
conn.close()
