import sqlite3
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path for uploaded files(images/png)
app.config['UPLOAD_FOLDER'] = "static/uploads/"

# Retrieves database connection
def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fetch badge detail with id as parameter
def get_badge(badgeId):
    conn = get_db_connection()
    badge = conn.execute('SELECT * FROM badges WHERE id = ?',(badgeId,)).fetchone()
    conn.close()
    if badge is None:
        abort(404)
    return badge

# Route for accessing and fetching all the badges
@app.route('/badges',methods=['GET'])
def listBadges():
    conn = get_db_connection()
    badges = conn.execute('SELECT * FROM badges').fetchall()
    conn.close()
    return render_template('badges.html', badges=badges)

# Index page with add badge form
@app.route('/',methods=['GET'])
@app.route('/badge/create', methods=['GET','POST'])
def createBadge():
    if request.method == "POST":
        f = request.files['badgeImage']
        filename = secure_filename(f.filename)
        file_path = app.config['UPLOAD_FOLDER'] + filename
        f.save(file_path)

        # badge tuple with attributes from request form
        badge = (request.form['badgeName'],request.form['badgeDescription'],file_path,request.form['eligibleStudents'])
        
        conn = get_db_connection()
        conn.execute("INSERT INTO badges (badgeName, badgeDescription, badgeImage, eligibleStudents) VALUES (?, ?, ?, ?)",badge)
        conn.commit()
        conn.close()
        return redirect(url_for('listBadges'))
    return render_template('create.html')

# Update page with badge id
@app.route('/badge/<int:id>/update', methods=['GET','POST'])
def updateBadge(id):
    badgeDetails = get_badge(id)
    if request.method == 'POST':
        if request.files['badgeImage']:
            # If the badge image is not updated
            f = request.files['badgeImage']
            filename = secure_filename(f.filename)
            file_path = app.config['UPLOAD_FOLDER'] + filename
            f.save(file_path)
            badge = (request.form['badgeName'],request.form['badgeDescription'],file_path,request.form['eligibleStudents'], badgeDetails['id'])
        else:
            # If the badge image is also updated, we update the path to image
            badge = (request.form['badgeName'],request.form['badgeDescription'],badgeDetails['badgeImage'],request.form['eligibleStudents'], badgeDetails['id'])
        conn = get_db_connection()
        conn.execute("UPDATE badges SET badgeName = ?, badgeDescription = ?, badgeImage = ?, eligibleStudents = ? WHERE id = ?", badge)
        conn.commit()
        conn.close()
        return redirect(url_for('listBadges'))
    return render_template('update.html', badge=badgeDetails)

# Delete endpoint with badge id as parameter, redirects back to badges directory
@app.route('/badge/<int:id>/delete', methods=['GET','DELETE'])
def deleteBadge(id):
    badge = get_badge(id)
    conn = get_db_connection()
    conn.execute("DELETE FROM badges WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listBadges'))

# Verification endpoint which takes "name" and "email" from request.form and searches across list of eligible students
# Returns path to badge image if authorized else returns 403 status code with message 
@app.route('/badge/verify', methods=['GET','POST'])
def verifyBadge():
    badgeName = request.form['name']
    email = request.form['email']
    conn = get_db_connection()
    badges = conn.execute("SELECT * FROM badges WHERE badgeName= ?",(badgeName,)).fetchone()
    conn.close()
    eligibleStudents = badges['eligibleStudents']
    eligibleStudents = eligibleStudents.lstrip('[').rstrip(']').split(',')
    
    if email in eligibleStudents:
        return jsonify({'badge':'http://localhost:5000/'+badges['badgeImage'],'message':'Congratulations for your achievement'}), 200
    return jsonify({'message':'Oops! No record found. Please contact administrator.'}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)