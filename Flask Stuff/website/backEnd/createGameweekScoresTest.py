import sqlite3


conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()
c.execute('SELECT * FROM gameweekScores')
ans = c.fetchall()
for i in ans:
    print(i)
c.close()
conn.close()