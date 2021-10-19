from fastapi.testclient import TestClient
from api.ImportApi import app
from tests.json_test_data import *

client = TestClient(app)

def test_correct_post():
    postItem = correctJson
    response = client.post("/uploadJsonDoc/", postItem)
    assert response.status_code == 200
    assert response.json() == "Json file successfully created"

def test_incorrect_post():
    postItem = incorrectJson
    response = client.post("/uploadJsonDoc/", postItem)
    assert response.status_code == 403
    assert response.json()["detail"] == "Json file not following schema"