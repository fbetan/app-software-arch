#!/usr/bin/env python3
import sys
import sqlite3
from flask import request, render_template
from project.database_model import db, Politician
from project import create_app

app = create_app()

with app.app_context():
    db.create_all()

@app.route("/")
def main():
    politicians = Politician.query.all()
    return render_template("index.html", 
                           politicians = politicians)

@app.route("/search", methods = ['POST'])
def search():
    if request.args.get("f") == "state":
        state = request.form['state']
        try:
            politicians = Politician.query.filter_by(state=state).all()
            count = Politician.query.filter_by(state=state).count()
            return render_template('search.html',
                                   count = count,
                                   state = state,
                                   politicians = politicians)
      
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





# pikaconn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = pikaconn.channel()

# channel.queue_declare(queue="search")
# channel.basic_publish(exchange='',routing_key='search',)