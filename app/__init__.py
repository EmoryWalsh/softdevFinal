from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/myshelves')
def myshelves():
    return render_template("myshelves.html")

@app.route('/bookfinder')
def bookfinder():
    return render_template("bookfinder.html")

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
