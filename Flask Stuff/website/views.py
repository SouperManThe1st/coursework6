from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
import sqlite3
from website.backEnd.userClub import getUsersClub
from website.backEnd.activeSquad import getPackPlayersDetails,IsPlayerTeamActive,getAllGameweeks,getAllFormations,getCurrentFormationID, getFormationName,updateFormation,getUpcomingFixtures,getCurrentGameweekID,orderByPosition,retrieveSquadPoints,getSquadPoints,addPlayerToSquad, getClubPlayers, getClubPlayerDetails, viewSquad, getPriceWhenPacked, removePlayerFromClub, createStarterSquad, getPlayerPosition
from website.backEnd.addClub import addClubMain
from website.backEnd.packs import  getPrice, keepPlayer, sellPlayer, openStarterPack, generatePack, generatePlayerPool, getBalance, updateBalance


views = Blueprint('views', __name__)

from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

def dontcache(view):
    @wraps(view)
    def dont_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(dont_cache, view)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():#IF TAKING TIME TO LOAD ON BROWSER THEN GO TO TERMINAL AND SELECT SQUAD
    userID = current_user.id
    clubID = getUsersClub(userID)
    if clubID == -1:
        addClubMain(userID)
        clubID = getUsersClub(userID)
        openStarterPack(clubID)
        yetToBeSelectedClubPlayers = getClubPlayers(clubID)
        formationID = 1
        createStarterSquad(yetToBeSelectedClubPlayers,clubID,formationID)
    clubPlayers = getClubPlayers(clubID)
    clubsPlayerInfo = getClubPlayerDetails(clubID)
    yetToBeSelectedClubPlayers = clubPlayers
    squad = viewSquad(clubID)

    currentFormationID = getCurrentFormationID(clubID)
    print(currentFormationID)
    currentFormationStructure = getFormationName(currentFormationID)
    formations = getAllFormations()
    #every Thursday at 12:00
    #currentGameweek = getCurrentGameweekID()
    #setThisWeeksSquad(clubID,currentGameweek-1) #Only for test purposes
    #setThisWeeksSquad(clubID,currentGameweek)#What's actually meant to happen

    lastGameweek = getCurrentGameweekID()-1
    getSquadPoints(clubID,lastGameweek)
    points = retrieveSquadPoints(clubID,lastGameweek)
    if len(squad) == 0:
        #slots = ['GK','DF','DF','DF','DF','MF','MF','MF','MF','FW','FW','FW']
        slots = createStarterSquad(yetToBeSelectedClubPlayers,clubID)  
        #makeStarterSquad(clubID)
        flash('Check out your club to see all your players!', category='success') 

    squad = viewSquad(clubID)
    squadPlayersIDs = []
    for player in squad:
        squadPlayersIDs.append(player[3])
    upcomingFixtures = getUpcomingFixtures()
    #ans2 = playerStats.query.order_by(playerStats.name)
    return render_template("home.html",currentFormationStructure = currentFormationStructure, formations = formations ,upcomingFixtures = upcomingFixtures ,lastGameweek = lastGameweek,user=current_user,clubID = clubID,squad = squad, clubPlayers = clubPlayers, clubsPlayerInfo = clubsPlayerInfo,squadPlayersIDs = squadPlayersIDs, points = points)


@views.route('/change-formation',methods=['GET', 'POST'])
@login_required
def change_formation():
    try:
        if request.method == 'POST':
            if request.form['formationID']:
                formationID = request.form['formationID']
                userID = current_user.id
                clubID = getUsersClub(userID)
                yetToBeSelectedClubPlayers = getClubPlayers(clubID)
                createStarterSquad(yetToBeSelectedClubPlayers,clubID,formationID)
                updateFormation(clubID,formationID)
                return redirect(url_for('views.home'))
    except:
        return redirect(url_for('views.home'))

@views.route('/edit-squad',methods=['GET', 'POST'])
@login_required
def edit_squad():
    try:
        if request.method == 'POST':
            if request.form['playerID']:
                userID = current_user.id
                clubID = getUsersClub(userID)
                squad = viewSquad(clubID)
                index = request.form.get("index")
                squadPlayersIDs = []
                for player in squad:
                    squadPlayersIDs.append(player[3])
                playerID = request.form.get("playerID")
                assert '(' not in playerID and playerID not in squadPlayersIDs, flash("That player is already in the squad",category='error')
                    #flash("You cannot add the same player to the squad",category='error')
                    #return redirect(url_for('views.home'))
                addPlayerToSquad(playerID,index,clubID)
                if IsPlayerTeamActive(playerID) == False:
                    flash("This player's team does not have a game in the upcoming gameweek", category = 'error')
                return redirect(url_for('views.home'))
    except:
        return redirect(url_for('views.home'))


@views.route('/my-club')
@login_required
def my_club():
    userID = current_user.id
    clubID = getUsersClub(userID)
    clubPlayers = getClubPlayers(clubID)
    clubPlayers = orderByPosition(clubPlayers)
    pricesWhenPacked = {}
    currentPrices = {}
    for playerID in clubPlayers:
        pricesWhenPacked[playerID] = (getPriceWhenPacked(playerID))
        currentPrices[playerID] = getPrice(playerID)
    balance = getBalance(clubID)
    clubsPlayerInfo = getPackPlayersDetails(clubPlayers)
    return render_template("my_club.html",user=current_user,clubID = clubID,clubsPlayerInfo = clubsPlayerInfo,pricesWhenPacked = pricesWhenPacked, currentPrices = currentPrices,balance = balance)

@views.route('/deal-with-my-club',methods=['GET', 'POST'])
@login_required
def deal_with_my_club():
    if request.method == 'POST':
        if request.form['decision'] == 'sell':
            playerID = request.form.get("playerID")
            playerPosition = getPlayerPosition(playerID)
            clubID = request.form.get("clubID")
            #clubsPlayers = getClubPlayers(clubID)
            ClubPlayersDetails = getClubPlayerDetails(clubID)
            positionCount = []
            minimum = ['GK','GK','DF','DF','DF','DF','DF','MF','MF','MF','MF','FW','FW','FW','FW']
            for player in ClubPlayersDetails:
                positionCount.append(player[1])
            if positionCount.count(playerPosition) > minimum.count(playerPosition):
                sellPlayer(playerID,clubID)
                removePlayerFromClub(clubID,playerID)
            else:
                flash('Cannot sell this player - too few in this position !', category='error')
    return redirect(url_for('views.my_club'))

@views.route('/view-player-<playerID>')
@login_required
def view_player(playerID):
    #return playerID
    userID = current_user.id
    clubID = getUsersClub(userID)
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute('SELECT * FROM playerStats WHERE IDnumber = ?',(playerID,))
    ans = c.fetchall()[0]
    c.close()
    conn.close()
    playerID = ans[0]
    name = ans[1]
    nation = ans[2]
    position = ans[3]
    team = ans[4]
    age = ans[5]
    appearances = ans[6]
    starts = ans[7]
    minutes = ans[8]
    goals = ans[9]
    assists = ans[10]
    penaltiesScored = ans[11]
    penaltiesAttempted = ans[12]
    yellowCards = ans[13]
    redCards = ans[14]
    minsPerGoal = ans[15]
    if minsPerGoal == 0:
        minsPerGoal = 'N/A'
    minsPerAssist = ans[16]
    if minsPerAssist == 0:
        minsPerAssist = 'N/A'
    return render_template('view_player.html',user = current_user, clubID = clubID,playerID = playerID, name = name, nation = nation, position = position, team = team, age = age, appearances = appearances, starts = starts, minutes = minutes, goals = goals, assists = assists, penaltiesScored = penaltiesScored,penaltiesAttempted = penaltiesAttempted, yellowCards = yellowCards, redCards = redCards, minsPerGoal = minsPerGoal, minsPerAssist = minsPerAssist )




@views.route('/store')
@login_required
@dontcache
def store():
    userID = current_user.id
    clubID = getUsersClub(userID)
    balance = getBalance(clubID)
    return render_template("store.html", user=current_user,balance = balance)


rarityDict = {'B':[10,5,2,1],'A':[2,2,2,1],'S':[1,2,2,2],'U':[1,5,10,10]}
conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()
c.execute('SELECT IDnumber, name,currentPrice FROM playerStats ORDER BY currentPrice')
ans = c.fetchall()
c.close()
conn.close()


@views.route('supreme-pack')
@dontcache
@login_required
def supreme_pack():
    userID = current_user.id
    clubID = getUsersClub(userID)
    balance = getBalance(clubID)
    if balance < 600:
        flash('Cannot afford this pack', category='error')
        return redirect(url_for('views.store'))
    else:
        pack = generatePack(generatePlayerPool(ans,rarityDict,'S'))
        newBalance = balance - 600
        updateBalance(newBalance,clubID)
        #newBalance, newPlayers = dealWithPack(pack)
        #updateDataBaseAfterPack(newBalance,newPlayers,clubID)
        packDisplay = getPackPlayersDetails(pack)
        price = getPrice(pack[0])
        packSize = len(pack)
        return render_template("supreme_pack.html",user=current_user,clubID = clubID,packDisplay = packDisplay,pack = pack,packSize = packSize,price = price)

@views.route('advanced-pack')
@dontcache
@login_required
def advanced_pack():
    userID = current_user.id
    clubID = getUsersClub(userID)
    balance = getBalance(clubID)
    if balance < 400:
        flash('Cannot afford this pack', category='error')
        return redirect(url_for('views.store'))
    else:
        pack = generatePack(generatePlayerPool(ans,rarityDict,'A'))
        newBalance = balance - 400
        updateBalance(newBalance,clubID)
        #newBalance, newPlayers = dealWithPack(pack)
        #updateDataBaseAfterPack(newBalance,newPlayers,clubID)
        packDisplay = getPackPlayersDetails(pack)
        price = getPrice(pack[0])
        packSize = len(pack)
        return render_template("advanced_pack.html",user=current_user,clubID = clubID,packDisplay = packDisplay,pack = pack,packSize = packSize,price = price)


@views.route('basic-pack')
@dontcache
@login_required
def basic_pack():
    userID = current_user.id
    clubID = getUsersClub(userID)
    balance = getBalance(clubID)
    if balance < 200:
        flash('Cannot afford this pack', category='error')
        return redirect(url_for('views.store'))
    else:
        pack = generatePack(generatePlayerPool(ans,rarityDict,'B'))
        assert len(pack) == 1
        newBalance = balance - 200
        updateBalance(newBalance,clubID)
        packDisplay = getPackPlayersDetails(pack)
        price = getPrice(pack[0])
        packSize = len(pack)
        return render_template("basic_pack.html",user=current_user,clubID = clubID,packDisplay = packDisplay,pack = pack,packSize = packSize,price = price)



@views.route('deal-with-pack',methods=['GET', 'POST'])
@login_required
def deal_with_pack():
    userID = current_user.id
    clubID = getUsersClub(userID)
    balance = getBalance(clubID)
    #if balance < 200:
        #return redirect(url_for('views.store'))
    if request.method == 'POST':
        if request.form['decision'] == 'keep':
            playerID = request.form.get("playerID")
            clubID = request.form.get("clubID")
            keepPlayer(playerID,clubID)
        else:
            playerID = request.form.get("playerID")
            clubID = request.form.get("clubID")
            sellPlayer(playerID,clubID)
        return redirect(url_for('views.store'))


@views.route('/my-profile')
@login_required
def my_profile():
    userID = current_user.id
    clubID = getUsersClub(userID)
    lastGameweek = getCurrentGameweekID() - 1
    allGameweeks = getAllGameweeks(clubID)
    return render_template("my_profile.html",user=current_user,clubID = clubID,allGameweeks = allGameweeks,lastGameweek = lastGameweek)




@views.route('/view-all-players',methods=['GET', 'POST'])
def view_all_players():
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute('SELECT IDnumber,name,position,team,currentPrice FROM playerStats ORDER BY currentPrice DESC')
    ans = c.fetchall()
    c.execute('SELECT Count(IDnumber) FROM playerStats')
    ans2 = c.fetchall()[0][0]
    c.close()
    conn.close()
    return render_template("view_all_players.html",playerStats = ans,numPlayers = ans2,user = current_user)


@views.route('/view-player-stats',methods=['GET', 'POST'])
def view_player_stats():
    statistics = ["goals","assists","yellowCards","redCards","minutes"]
    currentStat = "goals"
    return render_template("view_player_stats.html",statistics = statistics,currentStat = currentStat,user = current_user)


@views.route('/view-statistic')
def view_statistic(statistic):
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute(f'SELECT IDnumber,name,position,team,{statistic} FROM playerStats GROUP BY IDnumber HAVING {statistic} > 0 ORDER BY {statistic} DESC')
    ans = c.fetchall()
    return ans
    

@views.route('/view-stats',methods=['GET', 'POST'])
def view_stats():
    #try:
        statistics = ["goals","assists","yellowCards","redCards","minutes"]
        currentStat = "goals"
        if request.method == 'POST':
            if request.form['statistic']:
                statistic = request.form['statistic']
                stats = view_statistic(statistic)
                return render_template("view_stat.html",playerStats = stats, statistic = statistic,statistics = statistics, currentStat = currentStat,user = current_user) 
    #except:
        return render_template("view_stat.html",playerStats = view_statistic('goals'), statistic = 'goals',statistics = statistics, currentStat = currentStat,user = current_user)



