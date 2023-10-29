import requests 
import json

# url = "http://127.0.0.1:8000/list-posts/"

# data = {
#     "title": "second_post",
#     "user": "v"
# }


# result = requests.get(url=url, json=data)

# print(result)



url = "http://127.0.0.1:8000/posts/3"

data = {
    "title": "last_post",
    "user": "v"
}

response = requests.get(url)

if response.status_code == 200:
    post = response.json(url = url, json = data)
    # print("Created Post:")
    print(post)
else:
    print(f"Failed with status code: {response.status_code}")
