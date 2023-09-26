#!/usr/bin/env python3

import sqlite3
import json
import sys
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pika

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///politicians.db'

db.init_app(app)

class Politician(db.Model):
    id = db.Column("search_id", db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(20))
    cid = db.Column(db.String(30))
    firstlast = db.Column(db.String(40))
    lastname = db.Column(db.String(30))
    party = db.Column(db.String(20))
    office = db.Column(db.String(30))
    gender = db.Column(db.String(2))
    first_elected = db.Column(db.String(6))
    phone = db.Column(db.String(15))
    fax = db.Column(db.String(15))
    website = db.Column(db.String(50))
    webform = db.Column(db.String(50))
    congress_office = db.Column(db.String(50))
    bioguide_id = db.Column(db.String(20))
    votesmart_id = db.Column(db.String(20))
    feccandid = db.Column(db.String(20))
    twitter_id = db.Column(db.String(30))
    youtube_url = db.Column(db.String(50))
    facebook_id = db.Column(db.String(50))

with app.app_context():
    db.create_all()

def search_state_politicians(state):
    api_key = "181b03bde6f910748664d4f7c1811fb3"
    base_url = "http://www.opensecrets.org/api/?method=getLegislators"
    response = requests.get(base_url + f"&id={state}&apikey={api_key}&output=json", timeout=120)
    response_list = response.json()['response']['legislator']
    for i in range(0, len(response_list)):
        attributes = response_list[i]['@attributes']
        new_entry = Politician(cid = attributes['cid'],
                            state = state,
                            firstlast = attributes['firstlast'],
                            lastname = attributes['lastname'],
                            party = attributes['party'],
                            office = attributes['office'],
                            gender = attributes['gender'],
                            first_elected = attributes['first_elected'],
                            phone = attributes['phone'],
                            fax = attributes['fax'],
                            website = attributes['website'],
                            webform = attributes['webform'],
                            congress_office = attributes['congress_office'],
                            bioguide_id = attributes['bioguide_id'],
                            votesmart_id = attributes['votesmart_id'],
                            feccandid = attributes['feccandid'],
                            twitter_id = attributes['twitter_id'],
                            youtube_url = attributes['youtube_url'],
                            facebook_id = attributes['facebook_id']
                                )
        db.session.add(new_entry)
        db.session.commit()
    politicians = Politician.query.filter_by(state=state).all()
    count = Politician.query.filter_by(state=state).count()
    return render_template('search.html', count=count, state=state, politicians=politicians)
# pikaconn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = pikaconn.channel()

# channel.queue_declare(queue="search")


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/search", methods = ['POST'])
def search():
    state = request.form.get("states")
    try:
        politicians = Politician.query.filter_by(state=state).all()
        count = Politician.query.filter_by(state=state).count()
        if count == 0:
            return search_state_politicians(state)
        return render_template('search.html', count = count, state = state, politicians = politicians)
    except sqlite3.OperationalError:
        try:
            search_state_politicians(state)
        except ValueError:
            sys.exit(0)
        
    # channel.basic_publish(exchange='',routing_key='search',)