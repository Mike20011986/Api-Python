import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
requests_types = ["GET", "POST", "PUT", "DELETE"]
answer = []
for i in range(4):
    method = requests_types[i].lower()
    for type in requests_types:
        if method == "get":
            response = requests.get(url, params={"method": type})

        elif method == "post":
            response = requests.post(url, data={"method": type})

        elif method == "put":
            response = requests.put(url, data={"method": type})

        elif method == "delete":
            response = requests.delete(url, data={"method": type})

# если нужно распечатать все запросы и ответы
#        print(method, type)
#        print(response.status_code)
#        print(response.text)

        if method == type.lower() and response.text == "Wrong method provided" or method != type.lower() and response.text == '{"success":"!"}':
            answer.append(method)
            answer.append(type)
            answer.append(response.status_code)
            answer.append(response.text)

print(*answer, sep="\n")