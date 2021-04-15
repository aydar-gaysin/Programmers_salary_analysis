import os
import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable


load_dotenv()

SJ_API_URL = 'https://api.superjob.ru/2.20/vacancies/'
HH_API_URL = 'https://api.hh.ru/vacancies/'
PROGRAMMING_LANGUAGES = [
    '1C', 'C', 'C++', 'C#', 'Dart', 'Go', 'Java', 'Javascript',
    'Objective-C', 'PHP', 'Python', 'Ruby', 'Rust', 'Scala', 'Swift', 'Typescript'
]


def load_hh_vacancies(hh_api_url, language):
    parameters = {
        'area': '1',
        'text': language,
    }
    response = requests.get(f'{hh_api_url}', params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response


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
        elif min_salary or max_salary == 0:
            salary = None
        else:
            salary = None
    else:
        salary = None
    return salary


def predict_rub_salary_hh(salary_data):
    if salary_data:
        min_salary = salary_data['from']
        max_salary = salary_data['to']
        currency = salary_data['currency']
        if currency == 'RUR':
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


def get_sj_vacancies_data():
    vacancies_analytics = []

    for programming_language in PROGRAMMING_LANGUAGES:
        vacancies_quantity = 0
        paid_vacancies_for_language = 0
        accumulated_salary = 0
        vacancies_ids = []

        for sj_page_number in range(10):
            api_response = load_sj_vacancies(SJ_API_URL, programming_language, sj_page_number)

            for vacancy in api_response['objects']:
                vacancy_id = str(vacancy['id'])

                if vacancy_id in vacancies_ids:
                    continue
                vacancies_ids.append(vacancy_id)
                salary = predict_rub_salary_sj(vacancy)
                vacancies_quantity += 1

                if salary is not None:
                    paid_vacancies_for_language += 1
                    accumulated_salary += predict_rub_salary_sj(vacancy)

        if paid_vacancies_for_language != 0:
            median_salary = int(accumulated_salary / paid_vacancies_for_language)
            vacancies_analytics.append(
                [programming_language, vacancies_quantity, paid_vacancies_for_language, median_salary])
    return vacancies_analytics


def get_hh_vacancies_data():
    vacancies_analytics = []

    for language in PROGRAMMING_LANGUAGES:
        api_response = load_hh_vacancies(HH_API_URL, language)
        vacancies_found = api_response['found']
        pages_found = api_response['pages']

        cashed_items = []
        vacancies_for_language = 0
        accumulated_salary = 0

        for page in range(pages_found):

            for item in range(20):
                cashed_items.append(api_response['items'])
                salary = predict_rub_salary_hh(api_response['items'][item]['salary'])

                if salary is not None:
                    vacancies_for_language += 1
                    accumulated_salary += predict_rub_salary_hh(api_response['items'][item]['salary'])

        median_salary = int(accumulated_salary / vacancies_for_language)
        vacancies_analytics.append(
            [language, vacancies_found, vacancies_for_language, median_salary])
    return vacancies_analytics


def create_terminal_table(vacancies_analytics, title):
    vacancies_analytics_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for dataset in vacancies_analytics:
        vacancies_analytics_table.append(dataset)

    table = AsciiTable(vacancies_analytics_table, title)
    print(table.table)


def main():
    sj_title = 'SuperJob Moscow'
    hh_title = 'HeadHunter Moscow'
    create_terminal_table(get_sj_vacancies_data(), sj_title)
    create_terminal_table(get_hh_vacancies_data(), hh_title)


if __name__ == "__main__":
    main()