#!/usr/bin/env python3
import sys
import os
import json
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pika

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from database_support.database_model import db, Politician


app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/francisco/Desktop/web_app_project/main/politicians.db'
db.init_app(app)

with app.app_context():
    db.create_all()



def get_state_politicians(state):

    api_key = "181b03bde6f910748664d4f7c1811fb3"
    base_url = "http://www.opensecrets.org/api/?method=getLegislators"
    response = requests.get(base_url + f"&id={state}&apikey={api_key}&output=json", timeout=120)
    response_list = response.json()['response']['legislator']
    return response_list


def add_politicians(response_list, state):
    
    for count, entry in enumerate(response_list, 0):
        attributes = entry['@attributes']
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


def get_industries(cid):
    


@app.route('/')
def main():
    return render_template("collect_index.html")

@app.route('/collect', methods = ['POST'])
def collect():
    state = request.form.get("states")
    current_count = Politician.query.filter_by(state=state).count()
    if current_count != 0:
        current_politicians = Politician.query.filter_by(state=state).all()
        return render_template('search.html', count = current_count, state = state, politicians = current_politicians)

    res_list = get_state_politicians(state)
    add_politicians(res_list, state)
    politicians = Politician.query.filter_by(state=state).all()
    count = Politician.query.filter_by(state=state).count()
    total_count = Politician.query.count()
    return render_template('collection.html', count = count, state = state, politicians = politicians, total_count = total_count)
    


    # pikaconn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = pikaconn.channel()

    # channel.queue_declare(queue='search')
    
    # def callback(ch,method,properties,body):
    #     body = json.loads(body)
    #     print(f" [x] Received {body}")

    # channel.basic_consume(queue='search',on_message_callback=callback,auto_ack=True)
    
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

    # #on receipt of message

    # channel.queue_declare(queue='parameters')
   




# if __name__=='__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)

    
