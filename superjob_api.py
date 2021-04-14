import os
import requests

from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

SJ_API_URL = 'https://api.superjob.ru/2.20/vacancies/'

programming_languages = [
    'Ruby', 'Javascript', 'Rust', 'Java', 'Python', 'PHP', 'C++', 'C#', 'Go', 'Swift',
    'Dart', 'Objective-C', 'Scala', 'Typescript', 'Программист C'
]


def load_sj_vacancies(sj_api_url, programming_language, sj_page_number):
    headers = {
        'X-Api-App-Id': os.getenv('SJ_API_SECRET_KEY'),
    }

    parameters = {
        'keyword': programming_language,
        'count': '100',
        'page': sj_page_number,
        'town': 'Москва',
        'catalogues': 48
    }
    response = requests.get(sj_api_url, headers=headers, params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response


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


sj_page_number = 0
vacancies_quantity = 0
paid_vacancies_for_language = 0
accumulated_salary = 0

for programming_language in programming_languages:
    for sj_page_number in range(10):
        api_response = load_sj_vacancies(SJ_API_URL, programming_language, sj_page_number)
        for vacancy in api_response['objects']:
            salary = predict_rub_salary_sj(vacancy)
            vacancies_quantity += 1
            if salary is not None:
                paid_vacancies_for_language += 1
                accumulated_salary += predict_rub_salary_sj(vacancy)

    median_salary = int(accumulated_salary / paid_vacancies_for_language)

    language_salary_data = {
        "vacancies_found": vacancies_quantity,
        "vacancies_processed": paid_vacancies_for_language,
        "average_salary": median_salary
    }

    pprint({programming_language: language_salary_data})

