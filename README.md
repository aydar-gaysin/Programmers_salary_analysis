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
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| C#                    | 33               | 4                   | 236250           |
| Go                    | 8                | 4                   | 144125           |
| Java                  | 34               | 11                  | 152000           |
| Javascript            | 125              | 36                  | 152069           |
| Objective-C           | 3                | 1                   | 265000           |
| PHP                   | 88               | 24                  | 125062           |
| Python                | 44               | 12                  | 171791           |
| Ruby                  | 9                | 6                   | 166083           |
| Scala                 | 2                | 2                   | 190000           |
| Swift                 | 7                | 1                   | 265000           |
| Typescript            | 33               | 14                  | 220214           |
+-----------------------+------------------+---------------------+------------------+
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| C#                    | 1825             | 1380                | 171394           |
| Dart                  | 50               | 27                  | 165444           |
| Go                    | 1222             | 930                 | 224400           |
| Java                  | 3978             | 1600                | 226500           |
| Javascript            | 4530             | 1800                | 212083           |
| Objective-C           | 280              | 112                 | 152875           |
| PHP                   | 2027             | 1900                | 217578           |
| Python                | 5214             | 1600                | 163000           |
| Ruby                  | 354              | 234                 | 159153           |
| Scala                 | 411              | 105                 | 214200           |
| Swift                 | 613              | 372                 | 203125           |
| Typescript            | 1252             | 1134                | 219222           |
+-----------------------+------------------+---------------------+------------------+
```
### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
Fork the repo. Copy api_main.py to your project directory.

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
Wait till script finishes collecting and processing data (~60 seconds).

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).