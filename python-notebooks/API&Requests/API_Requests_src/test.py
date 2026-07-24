import requests

session = requests.Session()
url = "https://httpbin.org/cookies"
response = session.get(url)
# print(session.cookies.get_dict()) # 輸出：{'user': 'Peter'}
print(response.json())