import os
from flask import Flask, session, request, redirect, render_template, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')


@app.route('/')
def hello():
    return render_template('index.html')

