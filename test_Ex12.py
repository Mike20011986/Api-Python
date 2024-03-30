import requests


class TestExercise11:
    def test_find_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")

        assert "x-secret-homework-header" in response.headers, "There is no secret-homework-header in response"
        assert response.headers["x-secret-homework-header"] == "Some secret value", "There is a response with other secret-homework-header value"
        headers = dict(response.headers)
        print(f'x-secret-homework-header: {headers["x-secret-homework-header"]}')
        print(*[f"{k}: {v}" for k, v in headers.items()], sep='\n')