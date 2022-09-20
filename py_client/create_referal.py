import requests
json = {
    'public_id':'public_id',
    'commission': 130.45,
    'user_id': 2,
    'refered_user_id': 4,
}
endpoint = 'http://127.0.0.1:8000/referrals/'
try:
    response = requests.post(endpoint, json=json)
    print(response.status_code)
    print(response.json())
except Exception as error:
    print(error)