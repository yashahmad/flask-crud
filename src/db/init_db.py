import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()
cur.execute("INSERT INTO badges (badgeName, badgeDescription, badgeImage, eligibleStudents) VALUES (?, ?, ?, ?)",
('Achievers','ACM ICPC 2022','achievement_badge.png',"['john@example.com','johnny@edx.com']")
)

conn.commit()
conn.close()