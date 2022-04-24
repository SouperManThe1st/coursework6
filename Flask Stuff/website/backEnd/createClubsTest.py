import sqlite3

try:
  conn = sqlite3.connect('pythonDB19.db')
  c = conn.cursor()
  c.execute('SELECT * FROM userClubs')
  ans = c.fetchall()
  for i in ans:
    print(i)
except:
  print("No existing database")