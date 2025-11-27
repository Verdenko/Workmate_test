# Скрипт по обработке csv файлов

Данный скрипт примимает на вход один или несколько файлов формата .csv.
1. Ищет уникальные позиции в столбце `position`
2. Вычисляет среднюю эффективность (`performance`) по каждой позиции
3. Выводит отчёт в консоль 

### Установка зависимостей
1.  pip install poetry
2.  poetry install


### Запуск скрипта:
poetry run python src/main.py --files [путь к файлу формата .csv ...] --report performance



### Пример отчёта в терминале
Отчёт: performance
────────────────────────────
Position             Avg Performance
1  DevOps Engineer               4.80
2  Backend Developer             4.83
3  Fullstack Developer           4.70
4  Data Scientist                4.65
5  Frontend Developer            4.67
6  Mobile Developer              4.60
7  QA Engineer                   4.50
