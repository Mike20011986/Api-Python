from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.first_name = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    def test_edit_just_created_user(self):
        # EDIT NAME
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_without_auth(self):
        # EDIT NAME
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Auth token not supplied", "Unexpected error text")

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            self.first_name,
            "Wrong name of the user after edit"
        )

    def test_edit_with_auth_at_other_user(self):
        # REGISTER OTHER USER
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2["email"]
        password2 = register_data2["password"]

        # LOGIN OTHER USER
        login_data = {
            'email': email2,
            'password': password2
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT NAME
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "This user can only edit their own data.", "Unexpected error text")

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            self.first_name,
            "Wrong name of the user after edit"
        )

    def test_edit_invalid_email(self):
        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT NAME
        new_email = "invalid_email_example.com"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Invalid email format", "Unexpected error text")

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            self.email,
            "Wrong name of the user after edit"
        )

    def test_edit_very_short_firstname(self):
        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT NAME
        new_name = "l"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "The value for field `firstName` is too short", "Unexpected error text")

        # GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            self.email,
            "Wrong name of the user after edit"
        )