from flask import Flask, render_template, url_for, session

from flask import request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)  
app.secret_key = "12345678qwerty"
client = MongoClient('localhost', 27017)
db = client.flask_db
# data = db.data
data = db["data"]
@app.route('/')  
def home():
    return render_template('index.html') 

# ================================ sign up ==================================================

@app.route('/signup', methods =['GET', 'POST'])  
def signup():
    print("signup function is called")
    msg = ''
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form and 'name' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        data.insert_one({'username':username, 'password': password, 'name':name})
        msg = 'Signup Successfully'
        if not username or not password or not name:
            msg = 'Please fill out the form !'
        return render_template('signup.html', msg = msg)
    return render_template('signup.html',msg=msg) 

# ================================== login ================================================

@app.route('/login', methods =['GET', 'POST']) 
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        user = data.find_one({'username': username})
        print(user)
        if user:
            # Set session to indicate successful login
            session['username'] = request.form['username']
            return redirect(url_for('database'))
        else:
            return render_template('login.html',msg="Incorrect password or username")
            
    return render_template('login.html')  

# ================================== database ================================================

@app.route('/database')  
def database():
    alldata=list(data.find({}))
    for index, item in enumerate(alldata, start=1):
        item['serial_number'] = index
    return render_template('database.html',data=alldata) 


if __name__ == '__main__':  
   app.run(debug = True)  