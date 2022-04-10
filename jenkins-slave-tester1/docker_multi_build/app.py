#!usr/bin/env python3
from flask import render_template
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/builder')
def builder():
    return render_template('builder.html')


@app.route('/runner')
def runner():
    return render_template('runner.html')