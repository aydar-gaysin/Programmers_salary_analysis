import os
import requests

from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

SUPERJOB_API_URL = 'https://api.superjob.ru/2.20/vacancies/'

headers = {
    'X-Api-App-Id': os.getenv('API_SECRET_KEY'),
}

parameters = {
    'order_field': 'date',
    'order_direction': 'desc',
    'count': '100'
}

response = requests.get(SUPERJOB_API_URL, headers=headers, params=parameters)
response.raise_for_status()
api_response = response.json()
for vacancy in api_response['objects']:
    pprint(vacancy['profession'])
