import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class PoliticianFunding(db.Model):
    cid = db.Column(db.String(30), primary_key = True)
    cand_name = db.Column(db.String(80))
    cycle = db.Column(db.String(4))
    origin = db.Column(db.String(80))
    source = db.Column(db.String(80))


class Industry(db.Model):
    industry_code = db.Column(db.String(50), primary_key = True)
    industry_name = db.Column(db.String(50))
    indivs = db.Column(db.String(50))
    pacs = db.Column(db.String(50))
    total = db.Column(db.String(50))