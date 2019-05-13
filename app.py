#!flask/usr/bin/python3
from flask import Flask, render_template, request
from helper import build_graph, get_recommendations, build_graph_from_file

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods = ['GET'])
def main_screen():
    return render_template("index.html")

@app.route('/user', methods = ["GET"])
def user_input():
    return render_template("user.html")

@app.route('/graph', methods=["GET"])
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

@app.route('/graphresult', methods = ['POST'])
def custom_recommendation_list():
    graph_file = request.files["file"]
    root_node = request.form['inputusername']
    network_graph = build_graph_from_file(graph_file)
    if root_node not in network_graph.nodes():
        return render_template('error.html', mainerror = "The specified node", suberror = "Is not a part of the uploaded graph file")
    return_stuff = get_recommendations(network_graph, root_node)

    return render_template('result.html', recommends = return_stuff)

