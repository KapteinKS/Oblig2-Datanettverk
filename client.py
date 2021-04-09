import requests
# TODO everything
BASE = "http://127.0.0.1:5000/api/"

response = requests.get(BASE + "users")
print(response.json())
