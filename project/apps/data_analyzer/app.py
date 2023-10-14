#!/usr/bin/env python3

from flask import request, render_template
from project.database_model import db, Politician, Funding
from project import create_app

app = create_app()

with app.app_context():
    db.create_all()

@app.route('/')
def main():
    politicians = Politician.query.all()
    fundings = Funding.query.all()
    return render_template("analyze_index.html",
                           politicians = politicians,
                           fundings = fundings)

@app.route('/analyze', methods = ['POST'])
def analyze():
    if request.args.get("f") == "pol":
        cid = request.form['cid']
        try:
            fundings = Funding.query.filter_by(cid=cid).all()
            name = fundings[0].cand_name
            return render_template('fundinginfo.html',
                                   name = name,
                                   fundings = fundings)
        except ValueError:
            print("Not found!")

    elif request.args.get("f") == "ind":
        industry_code = request.form['industry_code']
        fundings = Funding.query.filter_by(industry_code=industry_code).all()
        industry_name = fundings[0].industry_name
        return render_template('analyze_industry.html',
                               industry_name = industry_name,
                               fundings=fundings)

    else:
        print("I just a dumb")
