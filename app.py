from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods = ['POST'])
def main_screen():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def narcissism_recommend():
    name = request.form['inputusername']
    return_stuff = [(name, 1) for i in range(10)]
    return render_template('result.html', recommends = return_stuff)
