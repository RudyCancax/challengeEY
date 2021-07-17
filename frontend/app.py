from flask import Flask, render_template, request , redirect, url_for, flash
import requests, json
import sys
import time

URL_API = "http://localhost:8000/users/login"
TOKEN = ""


app = Flask(__name__)

@app.route('/')
def principal():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html") 

@app.route('/login', methods=['POST'])
def posteo():
    email = request.form['email']
    password = request.form['password']
    usuario = {
    "email": email,
    "password": password,
    }
    resp = requests.post("http://localhost:8000/users/login", data=json.dumps(usuario))
    print('MENSAJE API: ' + str(resp.status_code), file=sys.stdout)
    if str(resp.status_code)  == '200':   # Datos Incorrectos
        response = json.loads(resp.text)
        response = response["token"]
        print('ACEPTADO: ' + str(resp.status_code), file=sys.stdout)
        return redirect(url_for('home', token = str(response), error = resp.status_code))
    else: # Datos Correctos
        print('nooooooo ACEPTADO: ' + str(resp.status_code), file=sys.stdout)
        return redirect(url_for("login"))



@app.route('/home', methods=['GET'])
def home():
    token = request.args.get('token')
    # print('TOKEN (impreso HOME): ' + token, file=sys.stdout)
    return render_template("home.html", token=token)

@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html") 


if __name__ == '__main__':
    app.run(debug=True)