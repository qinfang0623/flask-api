import requests

BASE = "http://127.0.0.1:5000/"


print("\n====================\==============\==============\==============\========\n")

response = requests.post(BASE + 'video/1', {
    "name": "Hello World!", "views": 555, "likes": 10
})
print(response.json())

print("\n==============\n")

response = requests.get(BASE + 'video/1')
print(response.json())

print("\n==============\n")

response = requests.patch(BASE + 'video/1', {
    "name": "Hello World Again!", "likes": 110
})
print(response.json())

print("\n==============\n")

response = requests.get(BASE + 'video/1')
print(response.json())

print("\n==============\n")

response = requests.delete(BASE + 'video/1')
print(response.status_code)

print("\n==============\n")

response = requests.get(BASE + 'video/1')
print(response.json())

print("\n==============\n")
