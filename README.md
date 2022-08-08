# Flask CRUD 

> Digital badges is a CRUD application where you can 
- Create new badges and assign it to group of users
- Fetch badge details 
- Update badge details 
- Delete badge details
- Verify whether user is authorized for the badge
- Upload file locally / server
 
> Technology Used:
- Frontend: Bootstrap, Jinja template
- Backend: Python, Flask 
- Database: SQLite

  
#### Steps to run application

Step 1: Create Virtual Environment
```
virtualenv venv
```
Step 2: Activate virtual env
```
. venv/bin/activate
```
Step 3: Install dependencies
```
pip install -r requirements.txt
```
Step 4: Initialize Database
```
cd src/db/
python3 init_db.py
```
Step 4: Export Flask App
```
cd ..
export FLASK_APP=main
```
Step 5: Run Flask App
```
flask run
```

### Screenshots of Digital Badge Application

![Index Screen](/screenshots/Addbadge.png "Create Badge")

![Badge Directory](/screenshots/Listbagdes.png "List Badges")

![Update Badge](/screenshots/Updatebadges.png "Update Badge")

![Verify Badge](/screenshots/RequestSuccessful.png "Verify Badge Successful")

![Unauthorized Verify](/screenshots/UnsuccessfulResponse.png "Verify Badge Unsuccessful")


