import requests
json = {
    'username':'poju',
    'first_name': 'abdulganiu',
    'last_name': 'adegbite',
    'email': 'abdulganiu@gmail.com',
    'password': 'smart5441'
}
endpoint = 'http://127.0.0.1:8000/users/'
try:
    response = requests.post(endpoint, json=json)
    print(response.status_code)
    print(response.json())
except Exception as error:
    print(error)