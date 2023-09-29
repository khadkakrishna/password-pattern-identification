from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from src import pattern_identification
import logging

app = Flask(__name__)
app.debug = True

from tinydb import TinyDB, Query
db = TinyDB('db.json')
table = db.table('user')
query = Query()
loggedinuser=""

"""
DATABASE related function to do CRUD operations
"""
def get_all_user():
    logging.debug("DATABASE: get all users")
    return table.all()

def get_user(username):
    logging.debug("DATABASE: get details of user",username)
    return table.search(query.username == username)[0]

def get_user_pass(username):
    logging.debug("DATABASE: get password of user", username)
    return table.search(query.username == username)[0]['password']

def update_user_pass(username, password):
    logging.debug("DATABASE: update password of user", username)
    return table.update( {'password' : password}, query.username == username)
    
def get_security_questions(username):
    logging.debug("DATABASE: get security questions of user", username)
    return table.search(query.username == username)[0]['security_questions']

def update_security_questions(username, q1, a1, q2, a2):
    logging.debug("DATABASE: update security questions of user", username)
    return table.update({"security_questions" : {"q1": q1, "q2":q2, "answer1":a1, "answer2": a2}}, query.username==username)

def get_personal_details(username):
    logging.debug("DATABASE: get personal details of user",username)
    return table.search(query.username == username)[0]['personal_details']

def update_user_profile(username, firstName, lastName, companyEmail, personalEmail, phone, dob, nationality, address):
    logging.debug("DATABASE: update personal details of user",username)
    return table.update({"personal_details" : {"first_name": firstName, 'last_name': lastName, 'personalemail': personalEmail, 'companyemail': companyEmail, 'phone_number': phone, 'DOB': dob, 'address': address, 'nationality': nationality, 'employeeID': '76001512', 'company': 'Micro Focus Software India Pvt Ltd'}}, query.username==username)
 

"""
ROUTING: pages for accessing the backend
"""
@app.route("/")
@app.route("/login")
def login(): 
    logging.info("Login Page accessed")
    return render_template('login.html')

@app.route("/home", methods = ['POST', 'GET'])
def home(): 
    logging.info("Home page accessed")
    global loggedinuser 
    if loggedinuser =="":
        logging.info("user logged in", loggedinuser)
        loggedinuser = request.form.get('username')
    elif loggedinuser == None:
        loggedinuser = request.form.get('username')
    return render_template('home.html')

@app.route("/changePassword")
def changePassword(): 
    logging.info("Accessed change password page")
    return render_template('changePassword.html')

@app.route("/updateSecurity")
def updateSecurity(): 
    logging.info("Update user security questions details")
    return render_template('updateSecurity.html', data=get_security_questions(loggedinuser))

@app.route("/updateProfile")
def updateProfile(): 
    logging.info("Update user profile details")
    return render_template('updateProfile.html', data=get_personal_details(loggedinuser))


@app.route("/viewProfile", methods=['POST'])
def viewProfile(): 
    logging.info("View user profile details")
    return render_template('home.html', user_data=get_personal_details(loggedinuser), show_profile=True)


"""
ROUTING POST urls for update operations
"""

@app.route("/updateSecuritySettingsOp", methods=['POST'])
def updateSecuritySettingsOp():
    update_security_questions(loggedinuser, request.form.get("q1"), request.form.get("answer1"), request.form.get("q2"), request.form.get("answer2")) 
    return render_template('home.html')

@app.route("/updateUserProfileOp", methods=['POST'])
def updateUserProfileOp():
    update_user_profile(loggedinuser, request.form.get("firstName"), request.form.get("lastName"), request.form.get("companyEmail"), request.form.get("personalEmail"), request.form.get("phone"), request.form.get("DOB"),request.form.get("nationality"), request.form.get("address")) 
    return render_template('home.html')

@app.route("/changePasswordOperation", methods=['POST'])
def changePasswordOperation(): 
    if request.method == 'POST':
        if request.form.get('submit') == 'verify':
            messages = pattern_identification.find(loggedinuser, request.form.get('password'))
            if len(messages) > 0:
                enable = False
            else:
                enable = True
            return render_template('/changePassword.html', pswd=request.form.get('password'), msg=messages, enable=enable)
        else :
            update_user_pass(loggedinuser, request.form.get('password'))
            return render_template('home.html')


"""
app.py main method: starting point of the code
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0')