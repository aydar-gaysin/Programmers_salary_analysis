import requests

from pprint import pprint

HHRU_API_URL = 'https://api.hh.ru/vacancies/'


def load_vacancies(hhru_api_url, language):
    parameters = {
        'area': '1',
        'text': language,
    }
    response = requests.get(f'{hhru_api_url}', params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response


def predict_rub_salary(salary_data):
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


def main():
    programming_languages = [
        'Ruby', 'Javascript', 'Rust', 'Java', 'Python', 'PHP', 'C++', 'C#', 'Go', 'Swift',
        'Dart', 'Objective-C', 'Scala', 'Typescript', 'Программист C'
    ]

    for language in programming_languages:
        api_response = load_vacancies(HHRU_API_URL, language)
        vacancies_found = api_response['found']
        pages_found = api_response['pages']

        cashed_items = []
        vacancies_for_language = 0
        accumulated_salary = 0

        for page in range(pages_found):

            for item in range(20):
                cashed_items.append(api_response['items'])
                salary = predict_rub_salary(api_response['items'][item]['salary'])

                if salary is not None:
                    vacancies_for_language += 1
                    accumulated_salary += predict_rub_salary(api_response['items'][item]['salary'])

        median_salary = int(accumulated_salary / vacancies_for_language)

        language_salary_data = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_for_language,
            "average_salary": median_salary
        }

        pprint({language: language_salary_data})


if __name__ == "__main__":
    main()
