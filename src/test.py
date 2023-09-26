import unittest
from unittest.mock import MagicMock
from app import Politician
from app import search, search_state_politicians


class TestMainForm(unittest.TestCase):

    def test_state_len(self, state):
        self.assertEqual(len(state), 2)

    def test_search_state_politicians(self, state):



class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        self.politician = Politician()
        self.politician._get_cid = MagicMock(return_value=123456)

    def test_politician(self):
        
        
        mock_politician = Politician()
        mock_politician.cid = MagicMock(return_value=12345)
