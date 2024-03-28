import requests


class TestExercise11:
    def test_find_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

        assert "Set-Cookie" in response.headers, "There is no cookie in response"
        assert "HomeWork" in response.cookies, "There is a response with other cookie"
        assert response.cookies["HomeWork"] == "hw_value", "There is a response with other cookie value"
        cookies = dict(response.cookies)
        print(*[f"{k}={v}" for k, v in cookies.items()])