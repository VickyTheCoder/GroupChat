import requests

api_url = "http://127.0.0.1:8000/api/"

#Testcase for signup for admin - make sure admin404 is not there in the dataase
url = api_url + "register/"
data = {
    "first_name": "admin404",
    "last_name": "ln",
    "email": "admin404@gmail.com",
    "password": "pass",
    "is_admin_user": "true"
}
response = requests.post(url, data=data)
response = response.json()
status = "Passed" if "user" in response and response.get("user").get("first_name") == "admin404" else "Failed"
print("Test Case for new admin signup: ", status)

#Testcase for signup for normal user - make sure user404 is not there in the database
data = {
    "first_name": "user404",
    "last_name": "ln",
    "email": "user404@gmail.com",
    "password": "pass",
    "is_admin_user": "false"
}
response = requests.post(url, data=data)
response = response.json()
status = "Passed" if "user" in response and response.get("user").get("first_name") == "user404" else "Failed"
print("Test Case for new normal signup: ", status)

url = api_url + "login/"
data = {
    "email": "user1@gmail.com",
    "password": "pass",
}
response = requests.post(url, data=data)
response = response.json()
print(response)
token = "token" in response
if token:
    status = "Passed" if ("refresh" in response.get("token") and "access" in response.get("token")) else "Failed"
else:
    status = "Failed"
print("Test Case for login: ", status)

data = {
    "email": "user1@gmail.com",
    "password": "wrongcrendentials",
}
response = requests.post(url, data=data)
response = response.json()
print(response)
token = "token" in response
if token:
    status = "Failed" if ("refresh" in response.get("token") and "access" in response.get("token")) else "Passed"
else:
    status = "Passed"
print("Test Case for login: ", status)