import unittest
from fastapi.testclient import TestClient
from api.ImportApi import app
from tests.json_test_data import *
from unittest.mock import patch


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    @patch('file_io.FileWriter.FileWriter.add_to_queue')
    def test_correct_post(self, mock_queue):
        postItem = correctJson
        response = self.client.post("/uploadJsonDoc/", postItem)
        mock_queue.return_value = None
        assert response.status_code == 200
        assert response.json() == "Json file successfully created"

    @patch('file_io.FileWriter.FileWriter.add_to_queue')
    def test_incorrect_post(self, mock_queue):
        postItem = incorrectJson
        response = self.client.post("/uploadJsonDoc/", postItem)
        mock_queue.return_value = None
        assert response.status_code == 403
        assert response.json()["detail"] == "Json file not following schema"