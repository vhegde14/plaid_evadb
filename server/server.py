import os
import json

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')
load_dotenv()

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SANDBOX = os.getenv('PLAID_SANDBOX')

# unique client id, but I am manually setting for the time being
client_user_id = '12345'

host = plaid.Environment.Sandbox
configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SANDBOX,
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@app.route('/api')
def hello():
    return "Hello World"

@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    request = LinkTokenCreateRequest(
        products=[Products("auth")],
        client_name="Plaid EvaDB",
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(
            client_user_id=client_user_id
        )
    )
    response = client.link_token_create(request)
    return jsonify(response.to_dict())


if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8000)))