#!/usr/bin/env python3

import sqlite3
import json
import os
import sys
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pika
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from database_support.database_model import db, Politician




app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/francisco/Desktop/web_app_project/main/politicians.db'
db.init_app(app)




    
# pikaconn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = pikaconn.channel()

# channel.queue_declare(queue="search")


@app.route("/")
def main():
    politicians = Politician.query.all()
    return render_template("index.html", politicians = politicians)

@app.route("/search", methods = ['POST'])
def search():
    if request.args.get("f") == "state":
        state = request.form['state']
        try:
            politicians = Politician.query.filter_by(state=state).all()
            count = Politician.query.filter_by(state=state).count()
            return render_template('search.html', count = count, state = state, politicians = politicians)
        
        except sqlite3.OperationalError:
            try:
                print("error")
                # api_response = get_state_politicians(state)
                # return add_politicians(api_response,state)
            except ValueError:
                sys.exit(0)
    elif request.args.get("f") == "pol":
        firstlast = request.form['name']
        politicians = Politician.query.filter_by(firstlast=firstlast).all()
        return render_template('basicpolinfo.html',
                                politicians = politicians)
    else:
        print("I dunno man")


    # channel.basic_publish(exchange='',routing_key='search',)