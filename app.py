from flask import *
import time
import os

app = Flask(__name__,static_url_path='', static_folder='frontend/static',template_folder='frontend/templates')
port = int(os.environ.get("PORT", 5000))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)