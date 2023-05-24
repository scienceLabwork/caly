from flask import *
import time
import os
import sqlite3 as sql
import random
from enc import encrypt, decrypt
import msmtp
import socket
from datetime import datetime

app = Flask(__name__,static_url_path='', static_folder='frontend/static',template_folder='frontend/templates')
app.secret_key = 'calypsoismadebyrudrashah'
port = int(os.environ.get("PORT", 5000))

def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except socket.error:
        return None

def genimage(name):
    return "https://api.dicebear.com/6.x/initials/svg?seed="+name+"&bold=1&fontSize=45"

def genlink(mail):
    encmail = encrypt(mail)
    conn = sql.connect('users.sqlite')
    cur = conn.cursor()
    keyval = str(random.randint(100000,999999))
    #if already exists, delete it
    cur.execute("Delete from rpass where email=?",(mail,))
    cur.execute("Insert into rpass values(?,?,?)",(mail,keyval,time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    ip_address = get_local_ip()
    url = f'http://{ip_address}:5454/reset?mail='+str(encmail).replace("b'","").replace("'","")+'&keyval='+str(keyval)
    return url

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

@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    if request.method == 'POST':
        conn = sql.connect('users.sqlite')
        cur = conn.cursor()
        email = request.form['email']
        cur.execute("SELECT email FROM users WHERE email = ?",(email,))
        data = cur.fetchone()
        if data is None:
            flash('Email does not exist', 'error')
            return render_template('forgot.html',color='red')
        else:
            print(genlink(email))
            msmtp.sendmail(email,genlink(email))
            flash('Reset Mail link sent to your mail id successully', 'success')
            return render_template('forgot.html',color='green')
    return render_template('forgot.html')

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    if request.method == 'GET':
        arg1 = request.args.get('mail')
        arg1 = decrypt(arg1.replace(" ","+"))
        arg2 = request.args.get('keyval')
        conn = sql.connect('users.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT email,tstamp FROM rpass WHERE email = ? AND key = ?",(arg1,arg2))
        data = cur.fetchone()
        if data is None:
            print('NO data')
            return redirect(url_for('index'))
        else:
            tstamp1 = data[1]
            tstamp2 = time.strftime('%Y-%m-%d %H:%M:%S')
            if((datetime.strptime(tstamp2, '%Y-%m-%d %H:%M:%S') - datetime.strptime(tstamp1, '%Y-%m-%d %H:%M:%S')).total_seconds() <= 7200):
                session['passchangerequest'] = True
                return render_template('reset.html',mail=arg1)
            else:
                print('time')
                return redirect(url_for('index'))
    return redirect(url_for('index')) 

@app.route('/postreset', methods=['POST', 'GET'])
def postreset():
    if 'passchangerequest' in session:
        if request.method == 'POST':
            password = request.form['password']
            mail = request.form['token']
            conn = sql.connect('users.sqlite')
            cur = conn.cursor()
            password = encrypt(password)
            cur.execute("UPDATE users SET password = ? WHERE email = ?",(password,mail))
            conn.commit()
            conn.close()
            session.clear()        
            return render_template('resetack.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)