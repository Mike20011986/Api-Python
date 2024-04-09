import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    datalist = [
        {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
        }
    ]


    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotov_example.com'
        data = self.prepare_registration_data(email)

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 400)
        assert response1.content.decode('utf-8') == "Invalid email format", \
            f"Unexpected response content {response1.content}"

    @pytest.mark.parametrize('condition', datalist)
    def test_create_user_without_required_field(self, condition):
        data = condition

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The following required params are missed:" in response.content.decode('utf-8'), \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_short_name(self):
        data = self.prepare_registration_data()
        data["firstName"] = 'l'

        response2 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode('utf-8') == "The value of 'firstName' field is too short", \
            f"Unexpected response content {response2.content}"

    def test_create_user_with_very_long_name(self):
        data = self.prepare_registration_data()
        data["firstName"] = 'jbuyguynoij9hygytvhgbkmkJWKWEMFKLEWMFIWJFEWRHIUnjkhhbjkmlkojoinmmoiiubjhkmijiubhbmnlkjubhbjhnknjoiniubnjkniuhhbhjbjkhuiweffffffffffffffffeeefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffmlkmjnhbvgjbilhyugyubhjbuygyugvvgytygyfyttfvtyvgvgfcfgxdzsazcvhgvbjnfвакупкуппупку'

        response2 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode('utf-8') == "The value of 'firstName' field is too long", \
            f"Unexpected response content {response2.content}"