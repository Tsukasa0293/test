from flask import Flask, redirect, render_template, request, session, url_for
import random, re

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

@app.route('/')
def route():
    return render_template('trpg.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)