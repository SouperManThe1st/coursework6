import sqlite3

def getUsersClub(userID):
  try:
    conn = sqlite3.connect('pythonDB19.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userClubs WHERE userID = ?',(userID,))
    ans = c.fetchall()
    c.close()
    conn.close()
    if len(ans) != 0:
      clubID = ans[0][0]
      return clubID
    else:
      return -1
  except:
    print("No existing database")
    return None