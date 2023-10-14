from project.src.database_model import db, Politician, Funding
from flask import Flask

app = Flask('frontend/app')

def test_home(client):
    response = client.get('/')
    assert b'<title>Politician Search App</title>' in response.data

def test_state_search_form(client, app):
    response = client.post('/search?f=state', data={'state':'TX'})
    assert search().count == 40



# class TestApp(unittest.TestCase):

#     def setUp(self):
#         self.ctx = app.app_context()
#         self.ctx.push()
#         self.client = app.test_client()

#     def tearDown(self):
#         self.ctx.pop()

#     @patch('request.args.get')
#     def test_state_search(self, mock_get):
#         mock = MagicMock()
#         mock['f'] = 'state'
#         mock['state'] = 'TX'
#         mock_get.return_value = mock['f']
#         state = mock['state']
#         self.assertEqual(self.count, 40)


#     def test_search_name(self):
#         self.search().request.args.get("f") == "pol"
#         self.search().firstname = ""




