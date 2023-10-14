#!/usr/bin/env python3

import requests
from flask import request, render_template
from project.src.database_model import db, Politician, Funding
from project import create_app

app = create_app()

with app.app_context():
    db.create_all()

def add_state_politicians(state):

    api_key = "181b03bde6f910748664d4f7c1811fb3"
    base_url = "http://www.opensecrets.org/api/?method=getLegislators"
    response = requests.get(base_url + f"&id={state}&apikey={api_key}&output=json", timeout=120)
    response_list = response.json()['response']['legislator']
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


def add_funding_info(cid, cycle='2022'):
    api_key = "181b03bde6f910748664d4f7c1811fb3"
    base_url = "http://www.opensecrets.org/api/?method=candIndustry"
    response = requests.get(base_url + f"&apikey={api_key}&cid={cid}&cycle={cycle}&output=json", 
                            timeout=120)
    response_list = response.json()['response']
    cand_info = response_list['industries']['@attributes']
    response_industries = response_list['industries']['industry']
    for count, entry in enumerate(response_industries, 0):
        attributes = entry['@attributes']
        new_entry = Funding(
            cid = cand_info['cid'],
            cand_name = cand_info['cand_name'],
            cycle = cycle,
            origin = cand_info['origin'],
            source = cand_info['source'],
            industry_code = attributes['industry_code'],
            industry_name = attributes['industry_name'],
            indivs = attributes['indivs'],
            pacs = attributes['pacs'],
            total = attributes['total']
        )
        db.session.add(new_entry)
        db.session.commit()
    
    


@app.route('/')
def main():
    politicians = Politician.query.all()
    return render_template("collect_index.html",
                           politicians = politicians)

@app.route('/collect', methods = ['POST'])
def collect():
    if request.args.get("f") == "state":
        state = request.form.get("states")
        current_count = Politician.query.filter_by(state=state).count()
        if current_count != 0:
            current_politicians = Politician.query.filter_by(state=state).all()
            return render_template('search.html', 
                                   count = current_count, 
                                   state = state, 
                                   politicians = current_politicians)

        add_state_politicians(state)
        politicians = Politician.query.filter_by(state=state).all()
        count = Politician.query.filter_by(state=state).count()
        total_count = Politician.query.count()
        return render_template('collection.html', 
                               count = count, 
                               state = state, 
                               politicians = politicians, 
                               total_count = total_count)
    
    elif request.args.get("f") == "pol":
        cid = request.form['cid']
        current_count = Funding.query.filter_by(cid=cid).count()
        if current_count != 0:
            funding_info = Funding.query.filter_by(cid=cid).all()
            name = funding_info[0].cand_name
            return render_template('fundinginfo.html',
                                   name = name,
                                   funding_info = funding_info)
        
        add_funding_info(cid)
        funding_info = Funding.query.filter_by(cid=cid).all()
        name = funding_info[0].cand_name
        return render_template('fundinginfo.html',
                               name = name,
                               funding_info = funding_info)

    else:
        print("dunno again dude")

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

    
