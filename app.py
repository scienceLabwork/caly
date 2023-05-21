from flask import *
import time
import os
import sqlite3 as sql
from enc import encrypt, decrypt

app = Flask(__name__,static_url_path='', static_folder='frontend/static',template_folder='frontend/templates')
port = int(os.environ.get("PORT", 5000))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/postrud', methods=['POST', 'GET'])
def postrud():
    if request.method == 'POST':
        conn = sql.connect('users.sqlite')
        cur = conn.cursor()
        email = request.form['email']
        fname = request.form['name']
        password = request.form['password']
        password = encrypt(password)
        tstamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO users (email,fname,password,tstamp) VALUES (?,?,?,?)",(email,fname,password,tstamp))
        conn.commit()
        msg = "Record successfully added"
    return msg

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)