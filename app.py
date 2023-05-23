from flask import *
import time
import os
import sqlite3 as sql
import random
from enc import encrypt, decrypt

app = Flask(__name__,static_url_path='', static_folder='frontend/static',template_folder='frontend/templates')
app.secret_key = 'calypsoismadebyrudrashah'
port = int(os.environ.get("PORT", 5000))

def genimage(name):
    return "https://api.dicebear.com/6.x/initials/svg?seed="+name+"&bold=1&fontSize=45"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if 'email' in session:
        return redirect(url_for('calendar'))
    return render_template('login.html')

@app.route('/register')
def register():
    if 'email' in session:
        return redirect(url_for('calendar'))
    return render_template('register.html')

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

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
        cur.execute("SELECT email FROM users WHERE email = ?",(email,))
        data = cur.fetchone()
        check = False
        if data is None:
            check = False
        else:
            check = True
        if(check==False):
            cur.execute("INSERT INTO users (email,fname,password,tstamp) VALUES (?,?,?,?)",(email,fname,password,tstamp))
            conn.commit()
            conn.close()
            session['email'] = email
            session['fname'] = fname
            session['image'] = genimage(fname)
            return redirect(url_for('calendar'))
        else:
            flash('Email already exists', 'error')
            return render_template('register.html')
    return msg

@app.route('/postlud', methods=['POST', 'GET'])
def postlud():
    if request.method == 'POST':
        conn = sql.connect('users.sqlite')
        cur = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT email,password,fname FROM users WHERE email = ?",(email,))
        data = cur.fetchone()
        if data is None:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
        elif decrypt(data[1]) != password:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
        else:
            session['email'] = email
            session['fname'] = data[2]
            session['image'] = genimage(data[2])
            return redirect(url_for('calendar'))
    return msg

@app.route('/calendar')
def calendar():
    if 'email' in session:
        return render_template('calendar.html',avtarurl=session['image'])
    return redirect(url_for('index'))

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)