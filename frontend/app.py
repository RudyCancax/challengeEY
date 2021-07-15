from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def principal():
    return "<h1>HOLAAAA MUNDO FLASK</h1>"

@app.route('/login')
def login():
    return render_template(
        "index.html"
    ) 

@app.route('/home/<nombre>')
def loged(nombre):
    return "<h2>HOLAAAAA JOVEN, {}</h2>".format(nombre)

if __name__ == '__main__':
    app.run