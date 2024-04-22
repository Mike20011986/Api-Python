from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import allure


@allure.epic('Test user delete')
class TestUserDelete(BaseCase):
    def setup_method(self):
        # REGISTER
        self.register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=self.register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = self.register_data["email"]
        self.first_name = self.register_data["firstName"]
        self.password = self.register_data["password"]
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        response2 = MyRequests.post("/user/login",
                                    data={
                                        "email": self.email,
                                        "password": self.password
                                    }
                                    )

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.description('This test make chance to delete user with id=2')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_with_id_2(self):
        data_id_2 = {
            "username": "Vitaliy",
            "email": "vinkotov@example.com",
            "firstName": "Vitalii",
            "lastName": "Kotov"
        }
        data = dict(email='vinkotov@example.com', password='1234')

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected error text"
        )

        response3 = MyRequests.get(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_values_by_names(response3, data_id_2)

    @allure.description('Positive test user delete')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_delete_positive(self):
        # DELETE
        response3 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # CHECK DELETE USER
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", "Unexpected text in response"

    @allure.description('This test make chance to delete user with other token')
    @allure.severity(allure.severity_level.MINOR)
    def test_user_delete_negative(self):
        # LOGIN WITH OTHER DATA
        data = dict(email='vinkotov@example.com', password='1234')

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE USER WITH OTHER TOKEN
        response2 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected text error"
        )

        response3 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_values_by_names(response3, self.register_data)