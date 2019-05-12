#!flask/usr/bin/python3
from flask import Flask, render_template, request
from helper import build_graph

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods = ['POST'])
def main_screen():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def narcissism_recommend():
    name = request.form['inputusername']
    build_graph(name)
    return render_template('result.html', recommends = return_stuff)
