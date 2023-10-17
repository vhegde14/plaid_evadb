import os
import json

from dotenv import load_dotenv
from flask import request, Flask, jsonify
from flask_cors import CORS, cross_origin
import datetime

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')
load_dotenv()

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SANDBOX = os.getenv('PLAID_SANDBOX')

access_token = None
item_id = None
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
    link_token_request = LinkTokenCreateRequest(
        products=[Products("auth"), Products("transactions")],
        client_name="Plaid EvaDB",
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(
            client_user_id=client_user_id
        )
    )
    response = client.link_token_create(link_token_request)
    return jsonify(response.to_dict())

@app.route('/set_access_token', methods=['POST'])
def set_access_token():
    global access_token
    global item_id
    public_token = request.json['public_token']
    try:
        public_token_exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        response = client.item_public_token_exchange(public_token_exchange_request)
        access_token = response['access_token']
        item_id = response['item_id']
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)

@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 6, 1),
    )
    response = client.transactions_get(request)
    transactions = response['transactions']

    # Iterating through paginated transactions in case there is more
    while len(transactions) < response['total_transactions']:
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 6, 1),
            options=TransactionsGetRequestOptions(
                offset=len(transactions)
            )
        )
    response = client.transactions_get(request)
    transactions.extend(response['transactions'])
    
    return jsonify(response.to_dict())  

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8000)))