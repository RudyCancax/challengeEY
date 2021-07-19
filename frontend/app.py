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
    resp = requests.get( URL_API ) #Obtenemos los usuarios de la BD
    response = json.loads(resp.text)
    usuariosLocal = response
    guatemala = 0
    costarica = 0
    panama = 0
    elsalvador = 0
    nicaragua = 0
    total = 0
    male = 0
    female = 0

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
        
        if usuario['gender'] == 'Male':
            male = male + 1
        else:
            female = female + 1
    print('GUA: ' + str(guatemala) + 'CRC: ' + str(costarica) + 'PAN: ' + str(panama) + 'SLV: ' + str(elsalvador) + 'NIC: ' + str(nicaragua) + '  TOTAL: ' + str(total), file=sys.stdout)


    # print('conteo: ' + str(response), file=sys.stdout)
    return render_template("home.html", usuarios = usuariosLocal, editar = edit_user, usuario = usuario_editar, guatemala = guatemala, costarica = costarica, panama = panama, elsalvador = elsalvador, nicaragua = nicaragua, male = male, female = female)


@app.route('/home', methods=['POST'])
def createUser():
    # Add new user
    usuario = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "gender": request.form['dropdowngender'],
        "country": request.form['dropdowncountry']
    }
    requests.post( URL_API, data=json.dumps(usuario))
    return redirect(url_for("home"))

@app.route('/enable-edit/<string:id>/<string:first_name>/<string:last_name>/<string:email>/<string:password>/<string:gender>/<string:country>/<string:edit>')
def enableEdit(id, first_name, last_name, email, password, gender, country, edit):
    global edit_user
    edit_user = edit
    usr = usuarioaProcesar(id, first_name, last_name, email, password, gender, country)
    return redirect(url_for('home'))

@app.route('/edit', methods=['POST'])
def edit():
    global edit_user
    edit_user = False
    usuarioE = usuarioaProcesar(usuario_editar['id'], request.form['first_name'], request.form['last_name'],request.form['email'], request.form['password'], request.form['dropdowngender'], request.form['dropdowncountry'])
    requests.put( URL_API, data=json.dumps(usuarioE)) # User Update code
    # print('EDITADO CORRECTAMENTE:  ' +  str(usuarioE) + ' Resp: ' + res.text, file=sys.stdout)
    return redirect(url_for('home'))


@app.route('/delete/<string:id>/<string:first_name>/<string:last_name>/<string:email>/<string:password>/<string:gender>/<string:country>')
def delete(id, first_name, last_name, email, password, gender, country):
    user = usuarioaProcesar(id, first_name, last_name, email, password, gender, country)
    res = requests.delete( URL_API, data=json.dumps(user))
    # print('ELIMIIII: ' + res.text + ' ' + str(user), file=sys.stdout)
    return redirect(url_for('home'))


@app.route('/disable-edit')
def disableEdit():
    global edit_user
    edit_user = False
    usuarioaProcesar( '', '',  '', '',  '',  '',  '')
    return redirect(url_for('home'))


def usuarioaProcesar(id, first_name, last_name, email, password, gender, country):
    user = {
        "id": id,
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "password" : password,
        "gender": gender, 
        "country": country
    }
    global usuario_editar
    usuario_editar = user
    print('USUARIO: ' + str(usuario_editar), file=sys.stdout)
    return user

@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)