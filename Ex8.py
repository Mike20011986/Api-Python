from json.decoder import JSONDecodeError
import requests
import time


not_json = "Response is not a JSON format"
url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response1 = requests.get(url)

try:
    parsed_response_text1 = response1.json()
    token = parsed_response_text1["token"]
    seconds = float(parsed_response_text1["seconds"])
    seconds1 = seconds / 2

except JSONDecodeError:
    print(not_json)

time.sleep(seconds1)
response_with_token = requests.get(url, params={"token": token})
try:
    parsed_response_with_token = response_with_token.json()
    status = parsed_response_with_token["status"]

except JSONDecodeError:
    print(not_json)

if status == "Job is NOT ready":
    time.sleep(seconds)
    response_with_token = requests.get(url, params={"token": token})
    try:
        parsed_response_with_token = response_with_token.json()
        status = parsed_response_with_token["status"]
    except JSONDecodeError:
        print(not_json)
    if status == "Job is ready" and "result" in parsed_response_with_token:
        print(f'Тест успешно завершён. Вот результат: {parsed_response_with_token["result"]}')
    else:
        print("Что-то пошло не так")