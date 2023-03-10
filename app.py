from flask import Flask, redirect, render_template, request, url_for,session
import mysql.connector
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host='localhost',user='root',password='',database='flask')
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/Home')
def Home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validator', methods=['POST'])
def login_validator():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `flask_login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect(url_for('Home'))
    else:
        return redirect(url_for('login'))

@app.route('/add_user',methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute("""INSERT INTO `flask_login` (`user_id`,`name`,`email`,`password`) VALUES(NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()


    cursor.execute("""SELECT * FROM `flask_login` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/Home')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, port=5555)
