from os import remove
from flask import Flask, render_template, request , redirect, url_for, flash
import requests, json, jsonify
import sys
import time

URL_API = "http://localhost:8080/users"
edit_user = False
usuario_editar = {} 
usuariosLocal = []

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def principal():
    return redirect(url_for("login"))

@app.route('/login')
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
    resp = requests.post( URL_API, data=json.dumps(usuario))
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
    resp = requests.get( URL_API )
    response = json.loads(resp.text)
    usuariosLocal = response
    guatemala = 0
    costarica = 0
    panama = 0
    elsalvador = 0
    nicaragua = 0
    total = 0

    for usuario in response:
        total = total + 1
        if usuario['country'] == 'Guatemala':
            guatemala = guatemala + 1
        elif usuario['country'] == 'Costa Rica':
            costarica = costarica + 1
        elif usuario['country'] == 'Panama':
            panama = panama + 1
        elif usuario['country'] == 'El Salvador':
            elsalvador = elsalvador + 1
        else:
            nicaragua = nicaragua + 1
    print('GUA: ' + str(guatemala) + 'CRC: ' + str(costarica) + 'PAN: ' + str(panama) + 'SLV: ' + str(elsalvador) + 'NIC: ' + str(nicaragua) + '  TOTAL: ' + str(total), file=sys.stdout)


    # print('conteo: ' + str(response), file=sys.stdout)
    return render_template("home.html", usuarios = usuariosLocal, editar = edit_user, usuario = usuario_editar, guatemala = guatemala, costarica = costarica, panama = panama, elsalvador = elsalvador, nicaragua = nicaragua)


@app.route('/home', methods=['POST'])
def createUser():
    # Add new user
    usuario = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password']
    }
    requests.post( URL_API, data=json.dumps(usuario))
    # End Add new user
    return redirect(url_for("home"))

@app.route('/enable-edit/<string:id>/<string:first_name>/<string:last_name>/<string:email>/<string:password>/<string:edit>')
def enableEdit(id, first_name, last_name, email, password, edit):
    global edit_user
    edit_user = edit
    usr = usuarioaProcesar(id, first_name, last_name, email, password)
    return redirect(url_for('home'))



@app.route('/edit', methods=['POST'])
def edit():
    global edit_user
    edit_user = False
    usuarioE = usuarioaProcesar(usuario_editar['id'], request.form['first_name'], request.form['last_name'],request.form['email'], request.form['password'])
    res = requests.put( URL_API, data=json.dumps(usuarioE))
    # print('EDITADO CORRECTAMENTE:  ' +  str(usuarioE) + ' Resp: ' + res.text, file=sys.stdout)
    return redirect(url_for('home'))


@app.route('/delete/<string:id>/<string:first_name>/<string:last_name>/<string:email>/<string:password>')
def delete(id, first_name, last_name, email, password):
    user = usuarioaProcesar(id, first_name, last_name, email, password)
    res = requests.delete( URL_API, data=json.dumps(user))
    # print('ELIMIIII: ' + res.text + ' ' + str(user), file=sys.stdout)
    return redirect(url_for('home'))


def usuarioaProcesar(id, first_name, last_name, email, password):
    user = {
        "id": id,
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "password" : password
    }
    global usuario_editar
    usuario_editar = user
    # print('heyyyyyyyyyyyyyy: ' + str(usuario_editar), file=sys.stdout)
    return user

@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)