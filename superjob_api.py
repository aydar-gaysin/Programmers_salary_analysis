import os
import requests

from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

SUPERJOB_API_URL = 'https://api.superjob.ru/2.20/vacancies/'

headers = {
    'X-Api-App-Id': os.getenv('SJ_API_SECRET_KEY'),
}

parameters = {
    'keyword': 'Программист',
    'count': '100',
    'town': 'Москва',
    'catalogues': 48
}

response = requests.get(SUPERJOB_API_URL, headers=headers, params=parameters)
#response = requests.get(SUPERJOB_API_URL, headers=headers)
response.raise_for_status()
api_response = response.json()

vacancy = {}


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        min_salary = vacancy['payment_from']
        max_salary = vacancy['payment_to']
        if min_salary is None and max_salary:
            salary = max_salary * 0.8
        elif min_salary and max_salary is None:
            salary = min_salary * 1.2
        elif min_salary and max_salary:
            salary = (min_salary + max_salary) / 2
        else:
            salary = None
    else:
        salary = None
    return salary


for vacancy in api_response['objects']:
    salary = predict_rub_salary_sj(vacancy)
    pprint(f"{vacancy['profession']}, {vacancy['town']['title']}, {salary}")
    #pprint(f"{vacancy['profession']}")
    #pprint(vacancy)

