import sqlite3

conn = sqlite3.connect('pythonDB19.db')
c = conn.cursor()
c.execute(f'SELECT ROUND(AVG(matchPoints)) FROM playerMatches WHERE matchPoints')
ans = c.fetchall()
c.close()
conn.close()
score = ans[0][0]
print(score)
#print(len(ans))