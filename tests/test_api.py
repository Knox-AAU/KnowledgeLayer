import unittest
from fastapi.testclient import TestClient
from api.ImportApi import app
from tests.json_test_data import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_correct_post(self):
        postItem = correctJson
        response = self.client.post("/uploadJsonDoc/", postItem)
        assert response.status_code == 200
        assert response.json() == "Json file successfully created"

    def test_incorrect_post(self):
        postItem = incorrectJson
        response = self.client.post("/uploadJsonDoc/", postItem)
        assert response.status_code == 403
        assert response.json()["detail"] == "Json file not following schema"