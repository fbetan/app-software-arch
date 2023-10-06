#!/usr/bin/env python3
import sys
from dataclasses import dataclass
import os
import requests
import datetime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from database_support.database_model import db, Politician





app = Flask(__name__, template_folder= '.../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///politicians.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@dataclass
class Industry:
    industry_code: str 
    industry_name: str
    indivs: str
    pacs: str
    total: str



def get_industries(cid, cycle='2022'):
    api_key = "181b03bde6f910748664d4f7c1811fb3"
    base_url = "http://www.opensecrets.org/api/?method=candIndustry"
    response = requests.get(base_url + f"&apikey={api_key}&cid={cid}&cycle={cycle}&output=json", 
                            timeout=120)
    response_list = response.json()['response']
    response_industries = response_list['industries']['industry']
    industries = []
    for count, industry in enumerate(response_industries, 0):
        attributes = industry['@attributes']
        list_entry = Industry(
            industry_code = attributes['industry_code'],
            industry_name = attributes['industry_name'],
            indivs = attributes['indivs'],
            pacs = attributes['pacs'],
            total = attributes['total']
        )
        industries.append(list_entry)
    return industries
    



    



@app.route('/data_analyzer')
def analyze():
