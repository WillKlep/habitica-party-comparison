# from flask import Flask, jsonify, request
# import requests
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# # Retrieve the API credentials from environment variables
# HABITICA_API_USER = 'c6718f43-a737-40cf-9db1-e6df0b51fe9a'
# HABITICA_API_KEY = os.getenv('HABITICA_API_KEY')

# HABITICA_API_URL = 'https://habitica.com/api/v3'

# def habitica_headers():
#     return {
#         'x-api-user': HABITICA_API_USER,
#         'x-api-key': HABITICA_API_KEY,
#         'Content-Type': 'application/json',
#     }

# @app.route('/')
# def index():
#     return "Welcome to the Habitica Flask App"

# @app.route('/groups', methods=['GET'])
# def get_party_members():
#     url = f'{HABITICA_API_URL}/groups/ef0fe518-94df-4647-b0f2-94f1e3a9142f'
#     headers = habitica_headers()
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         groups = response.json()['data']
#         party_members = groups['quest']['members']
#         return jsonify(party_members)
#     else:
#         return jsonify({'error': 'Failed to retrieve groups'}), response.status_code

# if __name__ == '__main__':
#     app.run(debug=True)



import os
from flask import Flask, jsonify, render_template, request
import requests
import dotenv

app = Flask(__name__)

# load environment variables
dotenv.load_dotenv()

# Retrieve the API credentials from environment variables
HABITICA_API_USER = 'c6718f43-a737-40cf-9db1-e6df0b51fe9a'
HABITICA_API_KEY = os.getenv('HABITICA_API_KEY')
HABITICA_API_URL = 'https://habitica.com/api/v3'
HABITICA_PARTY_ID = 'ef0fe518-94df-4647-b0f2-94f1e3a9142f'

def habitica_headers():
    return {
        'x-api-user': HABITICA_API_USER,
        'x-api-key': HABITICA_API_KEY,
        'Content-Type': 'application/json',
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-ids')
def get_user_ids():
    # JSON object of party
    url = f'{HABITICA_API_URL}/groups/{HABITICA_PARTY_ID}/members'
    print(url)
    headers = habitica_headers()
    response = requests.get(url, headers=headers)

    print(f"My Response Status Code: {response.status_code}")
    # print(f"My Response Body: {response.text}")

    if response.status_code == 200:
        members = response.json()['data']
        user_ids = [member["_id"] for member in members]
        print(user_ids)
        return jsonify(user_ids)
    else:
        return jsonify({'error': 'Failed to retrieve party data'}), response.status_code

@app.route('/user/<user_id>')
def user_detail(user_id):
    url = f'{HABITICA_API_URL}/members/{user_id}'
    response = requests.get(url, headers=habitica_headers())
    if response.status_code == 200:
        user_info = response.json()['data']
        return jsonify({
            'username': user_info['profile']['name'],
            'level': user_info['stats']['lvl'],
            'className': user_info['stats']['class'],
            'gold': user_info['stats']['gp'],
            'currHealth': user_info['stats']['hp'],
            'maxHealth': user_info['stats']['maxHealth'],
            'currExp': user_info['stats']['exp'],
            'toNextLevelExp': user_info['stats']['toNextLevel'],
            'user_id': user_id
        })
    else:
        return jsonify({'error': 'Failed to retrieve user details'}), response.status_code
    
@app.route('/tasks')
def get_tasks():
    url = f'{HABITICA_API_URL}/tasks/user'
    response = requests.get(url, headers=habitica_headers())
    if response.status_code == 200:
        return response.json()['data']
    else:
        return jsonify({'error': 'Failed to retrieve user details'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
