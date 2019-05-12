#!flask/usr/bin/python3
from flask import Flask, render_template, request
from helper import build_graph, get_recommendations

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods = ['POST', 'GET'])
def main_screen():
    return render_template("index.html")

@app.route('/user', methods = ["POST", "GET"])
def user_input():
    return render_template("user.html")

@app.route('/graph', methods=["POST", "GET"])
def network_input():
    return render_template("network.html")

@app.route('/result', methods = ['POST'])
def recommendations_list():
    name = request.form['inputusername']
    user_graph = build_graph(name)
    if user_graph == False:
        return render_template("error.html", mainerror = "This github user", suberror = "Does not exist")
    return_stuff = get_recommendations(user_graph, name)
    return render_template('result.html', recommends = return_stuff)
