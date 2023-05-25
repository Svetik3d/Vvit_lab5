import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username != "" and password != "":
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                if records!=[]:
                    return render_template('account.html', full_name=records[0][1])
                else:
                    return render_template('error.html',
                                           err="There's no such user in the database")
            else:
                return render_template('error.html',
                                       err="It's impossible noy to enter anything")
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

"Реализовать обработку всех исключений при регистрации"

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name != "" and password != "" and login != "":
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
        else:
            return render_template('error.html',
                                   err="It's impossible noy to enter anything")
    return render_template('registration.html')

app.run()