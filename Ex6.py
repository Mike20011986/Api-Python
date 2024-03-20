import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

count_responses = len(response.history)
last_response = response

print(count_responses)
print(last_response.url)