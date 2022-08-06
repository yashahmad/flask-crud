import sqlite3
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/badges',methods=['GET'])
def listBadges():
    conn = get_db_connection()
    badges = conn.execute('SELECT * FROM badges').fetchall()
    conn.close()
    return render_template('badges.html', badges=badges)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)