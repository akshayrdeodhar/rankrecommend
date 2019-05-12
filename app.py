#!flask/usr/bin/python3
from flask import Flask, render_template, request
from helper import build_graph, get_recommendations

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods = ['POST', 'GET'])
def main_screen():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def recommendations_list():
    name = request.form['inputusername']
    user_graph = build_graph(name)
    return_stuff = get_recommendations(user_graph, name)
    return render_template('result.html', recommends = return_stuff)
