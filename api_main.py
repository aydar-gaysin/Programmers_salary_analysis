import os
import requests

from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable


SJ_API_URL = 'https://api.superjob.ru/2.20/vacancies/'
HH_API_URL = 'https://api.hh.ru/vacancies/'
MOSCOW_ID = '1'
CATALOGUE_ID = 48
PROGRAMMING_LANGUAGES = [
    'C++', #'C#', 'Dart', 'Go', 'Java', 'Javascript',
    #'Objective-C', 'PHP', 'Python', 'Ruby', 'Scala', 'Swift', 'Typescript'
]


def load_hh_vacancies(hh_api_url, language, sj_page_number):
    parameters = {
        'area': MOSCOW_ID,
        'text': language,
        'page': sj_page_number
    }
    response = requests.get(f'{hh_api_url}', params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response


def load_sj_vacancies(catalogue_id, sj_api_key, sj_api_url,
                      programming_language, sj_page_number):
    headers = {
        'X-Api-App-Id': sj_api_key,
    }

    parameters = {
        'keyword': programming_language,
        'count': '100',
        'page': sj_page_number,
        'town': 'Москва',
        'catalogues': catalogue_id
    }
    response = requests.get(sj_api_url, headers=headers, params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response


def calculate_average(min_salary, max_salary):
    if not min_salary and max_salary:
        salary = max_salary * 0.8
    elif min_salary and not max_salary:
        salary = min_salary * 1.2
    elif min_salary and max_salary:
        salary = (min_salary + max_salary) / 2
    return salary


def predict_rub_salary_sj(vacancy):
    min_salary = vacancy['payment_from']
    max_salary = vacancy['payment_to']
    currency = vacancy['currency']
    if currency != 'rub':
        return None
    if min_salary and max_salary:
        return calculate_average(min_salary, max_salary)


def predict_rub_salary_hh(salary_data):
    if not salary_data:
        return None
    min_salary = salary_data['from']
    max_salary = salary_data['to']
    currency = salary_data['currency']
    if currency != 'RUR':
        return None
    if min_salary and max_salary:
        return calculate_average(min_salary, max_salary)


def get_sj_vacancies(catalogue_id, programming_languages, sj_api_key,
                     sj_api_url):
    vacancies_analytics = []

    for programming_language in programming_languages:
        vacancies_quantity = 0
        paid_vacancies_for_language = 0
        accumulated_salary = 0
        vacancies_ids = []

        for sj_page_number in count():
            api_response = load_sj_vacancies(catalogue_id, sj_api_key,
                                             sj_api_url, programming_language,
                                             sj_page_number)
            for vacancy in api_response['objects']:
                vacancy_id = str(vacancy['id'])
                if vacancy_id in vacancies_ids:
                    continue
                vacancies_ids.append(vacancy_id)
                salary = predict_rub_salary_sj(vacancy)
                vacancies_quantity += 1
                if salary:
                    paid_vacancies_for_language += 1
                    accumulated_salary += salary

            if not api_response['more']:
                break

        if paid_vacancies_for_language:
            median_salary = int(accumulated_salary /
                                paid_vacancies_for_language)
            vacancies_analytics.append(
                [programming_language, vacancies_quantity,
                 paid_vacancies_for_language, median_salary])
    return vacancies_analytics


def get_hh_vacancies(programming_languages):
    vacancies_analytics = []

    for language in programming_languages:
        api_response = load_hh_vacancies(HH_API_URL, language, 0)
        vacancies_found = api_response['found']
        pages_found = api_response['pages']

        vacancies_for_language = 0
        accumulated_salary = 0

        for sj_page_number in range(pages_found):
            api_response = load_hh_vacancies(HH_API_URL, language,
                                             sj_page_number)
            for item in range(20):
                try:
                    salary = predict_rub_salary_hh(api_response['items'][item]
                                                   ['salary'])
                    if salary:
                        vacancies_for_language += 1
                        accumulated_salary += salary
                except IndexError:
                    break

        median_salary = int(accumulated_salary / vacancies_for_language)
        vacancies_analytics.append(
            [language, vacancies_found, vacancies_for_language, median_salary])
    return vacancies_analytics


def create_terminal_table(vacancies_analytics, title):
    vacancies_analytics_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
         'Средняя зарплата']
    ]

    for dataset in vacancies_analytics:
        vacancies_analytics_table.append(dataset)

    table = AsciiTable(vacancies_analytics_table, title)
    return table.table


def main():
    load_dotenv()
    sj_api_key = os.getenv('SJ_API_SECRET_KEY')
    sj_title = 'SuperJob Moscow'
    hh_title = 'HeadHunter Moscow'
    print(create_terminal_table(get_sj_vacancies(CATALOGUE_ID,
                                                 PROGRAMMING_LANGUAGES,
                                                 sj_api_key, SJ_API_URL),
                                sj_title))
    print(create_terminal_table(get_hh_vacancies(PROGRAMMING_LANGUAGES),
                                hh_title))


if __name__ == '__main__':
    main()
