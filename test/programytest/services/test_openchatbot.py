import unittest
import json

from programy.services.openchat import OpenChatRESTService
from programy.config.brain.service import BrainServiceConfiguration
from programy.services.openchatbots import OpenChatBot

from programytest.client import TestClient


class MockRestResponse(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class MockRestAPI(object):

    def __init__(self, status_code=200, response="REST response"):
        self.status_code = status_code
        self.response = response

    def get(self, host):
        return MockRestResponse(self.status_code, self.response)

    def post(self, host, data):
        return MockRestResponse(self.status_code, self.response)


class OpenChatRESTServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain._openchatbots._openchatbots['CHATBOT1'] = OpenChatBot("openchat1",
                                                                                         "http://localhost:5959/api/rest/v2.0/ask",
                                                                                         "GET")

    def test_ask_question_get(self):

        mock_data = {"response": {
                            "text": "Hi there from chatbot1",
                        },
                        "status": {"code": 200, "text": "success"}
                     }
        mock_response = json.dumps(mock_data)

        service = OpenChatRESTService(BrainServiceConfiguration("openchatbot"), api=MockRestAPI(200, mock_response))

        response = service.ask_question(self._client_context, "chatbot1 Hello")
        self.assertIsNotNone(response)
        self.assertEquals("Hi there from chatbot1", response)
