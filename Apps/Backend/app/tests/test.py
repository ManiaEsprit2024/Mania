import requests

url = 'http://127.0.0.1:5000/api/user/register'
data = {
    'username': 'test',
    'password': 'test'
}

response = requests.post(url, json=data)
print(response.json())
