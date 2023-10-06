import unittest
from unittest.mock import MagicMock
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from frontend.src.app import app, db, Politician, search, get_state_politicians, add_politicians



class TestMainForm(unittest.TestCase):

    def setUp(self):
        #db = SQLAlchemy()
        
        mock_object = {'response':
                       {'legislators': [
                           {'@attributes':
                            {'cid':'123456789',
                             'firstlast':'Fooby McBar',
                             'lastname':'McBar',
                             'party':'X',
                             'office':'XX01',
                             'gender':'N',
                             'first_elected':'Never',
                             'phone':'1800-not-a-number',
                             'fax':'a rare relic',
                             'website':'zzz.lolno.zom',
                             'webform':'none',
                             'congress_office':'the best one',
                             'bioguide_id':'guidebio',
                             'votesmart_id':'smarterest',
                             'feccandid':'didnaccef',
                             'twitter_id':'its x now',
                             'youtube_url':'ayoutube.zom',
                             'facebook_id':'foobymcfacemcbar'}
                           }
                           ]
                        }
                    }
        mock_json = json.dumps(mock_object)
        self.state = 'XX'
        
class TestDBSearch(unittest.TestCase):
    def setUp(self):
        temp_entry = Politician(cid = '123456789',
                                state = 'XX',
                                firstlast = 'Fooby McBar',
                                lastname = 'McBar',
                                party= 'X',
                                office = 'XX01',
                                gender = 'N',
                                first_elected = 'Never',
                                phone = '1800-not-a-number',
                                fax = 'a rare relic',
                                website = 'zzz.lolno.zom',
                                webform = 'none',
                                congress_office = 'the best one',
                                bioguide_id = 'guidebio',
                                votesmart_id = 'smarterest',
                                feccandid = 'didnaccef',
                                twitter_id = 'its x now',
                                youtube_url = 'ayoutube.zom',
                                facebook_id = 'foobymcfacemcbar')
        db.session.add(temp_entry)
        db.session.commit()

    
    def test_search(self):
        self.search().state = 'XX'
        mocktician = self.search().politicians
        self.assertEqual(search().count, 1)


    def test_search_state_politicians(self, state):



class TestDatabase(unittest.TestCase):
    
    
        

    def test_politician(self):
        
        
        mock_politician = Politician()
        mock_politician.cid = MagicMock(return_value=12345)
