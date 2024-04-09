from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def setup_method(self):
        self.unexpected_fields = ["email", "firstName", "lastName"]

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, self.unexpected_fields)

    def test_get_user_details_auth_at_same_user(self):
        response2 = MyRequests.get(
            f"/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_at_other_user(self):
        response3 = MyRequests.get(
            f"/user/1",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_has_key(response3, "username")
        Assertions.assert_json_has_not_keys(response3, self.unexpected_fields)