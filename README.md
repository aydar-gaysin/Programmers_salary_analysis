# Programming vacancies compare

This program gets all programming vacancies in Moscow city from HeadHunter & SuperJob portals through the appropriate
APIs. It processes vacancies data to retrieve:
- vacancies total quantity;
- quantity of jobs with a salary in the ruble currency and with an explicit indication of the minimum, maximum salary
  or salary fork;
- average salary for each programming language.

Finally, it builds two ASCII tables containing processed salaries data.

Example:

```
as for 29 Apr 2021:

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| C++                   | 36               | 31                  | 154806           |
| C#                    | 30               | 19                  | 153953           |
| Go                    | 10               | 8                   | 183937           |
| Java                  | 29               | 19                  | 152684           |
| Javascript            | 110              | 76                  | 133210           |
| Objective-C           | 1                | 1                   | 168000           |
| PHP                   | 93               | 65                  | 127415           |
| Python                | 50               | 29                  | 147172           |
| Ruby                  | 8                | 5                   | 200300           |
| Scala                 | 3                | 2                   | 190000           |
| Swift                 | 5                | 3                   | 156000           |
| Typescript            | 24               | 15                  | 216033           |
+-----------------------+------------------+---------------------+------------------+
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| C++                   | 1885             | 561                 | 160863           |
| C#                    | 1848             | 493                 | 160737           |
| Dart                  | 42               | 13                  | 161538           |
| Go                    | 1283             | 329                 | 157572           |
| Java                  | 3998             | 469                 | 200147           |
| Javascript            | 4556             | 896                 | 157088           |
| Objective-C           | 277              | 57                  | 203166           |
| PHP                   | 1991             | 915                 | 141652           |
| Python                | 5316             | 448                 | 173786           |
| Ruby                  | 353              | 100                 | 190755           |
| Scala                 | 384              | 55                  | 231436           |
| Swift                 | 625              | 153                 | 197378           |
| Typescript            | 1291             | 386                 | 188446           |
+-----------------------+------------------+---------------------+------------------+
```
### How to install

Python3 should be already installed.
Fork the repo. Copy files to your project directory.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to run

api_main.py: Edit programming languages list in global variable PROGRAMMING_LANGUAGES if needed:
```
PROGRAMMING_LANGUAGES = [
    '1C', 'C', 'C++', 'C#', 'Dart', 'Go', 'Java', 'Javascript',
    'Objective-C', 'PHP', 'Python', 'Ruby', 'Rust', 'Scala', 'Swift', 'Typescript'
]
```

Start script:
```
python api_main.py
```
Wait till script finishes collecting and processing data (~5 minutes).

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).