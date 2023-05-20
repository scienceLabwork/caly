from flask import *
import time
import os

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
    #Database Structure users(email TEXT, fname TEXT, password TEXT, tstamp TEXT, ex1 TEXT, ex2 TEXT);
    msg = ''
    if request.method == 'GET':
        try:
            email = request.form['email']
            fname = request.form['fname']
            password = request.form['password']
            tstamp = time.strftime('%Y-%m-%d %H:%M:%S')
            with sql.connect("users.sqlite") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (email,fname,password,tstamp,ex1,ex2) VALUES (?,?,?,?,?,?)",(email,fname,password,tstamp,'0','0') )
                con.commit()
                msg = "Record successfully added"
                print(msg)
        except:
            con.rollback()
            msg = "error in insert operation"
            return msg
            print(msg)
        finally:
            return msg
            con.close()
    return msg

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)