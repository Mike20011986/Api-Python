import json.decoder
from requests import Response
import json
from datetime import datetime


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None, username=None):
        if email is None:
            basepart = "learnqa"
            domain = "example.com"
            randompart = datetime.now().strftime("%m%d%y%H%M%S")
            email = f"{basepart}{randompart}@{domain}"

        if username is None:
            username = 'learnqa'

        return {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }