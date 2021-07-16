from flask import Flask, render_template, request
import requests, json


URL_API = "http://localhost:8000/users/login"

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template("login.html")

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
    return 'Hola ' + email + ' ' + password + ' ' + resp.text



@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html") 


if __name__ == '__main__':
    app.run