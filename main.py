import argparse
import csv
import os
from tabulate import tabulate
from collections import defaultdict
from typing import List, Dict, Any, Callable

def main() -> None:
    
    parser = argparse.ArgumentParser(
        description="Генератор отчётов по сотрудникам из CSV-файлов"
    )
    parser.add_argument(
        '--files',
        nargs='+',
        metavar='FILE',
        required=True,
        type=validate_file_extension,
        help="Пути к одному или нескольким CSV-файлам с данными сотрудников"
    )
    parser.add_argument(
        '--report',
        choices=REPORTS.keys(),
        required=True,
        help="Тип отчёта для генерации"
    )

    args = parser.parse_args()

    employees = read_employees_from_files(args.files)

    try:
        if not employees:
            print("Не удалось прочитать данные из файлов.")
            raise ValueError("Нет данных сотрудников.")
    except Exception as e:
        print(f"Ошибка: {e}")
        parser.print_help()

    report_data = REPORTS[args.report](employees)

    print_report(args.report, report_data)

def validate_file_extension(filepath):
    """ Проверяет расширение файла """

    _, extension = os.path.splitext(filepath)
    if extension.lower() not in ['.csv']:
        raise argparse.ArgumentTypeError("Поддерживаются только файлы с расширением .csv")
    return filepath

def read_employees_from_files(filenames: List[str]) -> List[Dict[str, str]]:
    """ Читает все CSV-файлы и возвращает список словарей-сотрудников """
    employees = []
    for filename in filenames:
        with open(filename, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            if 'position' not in reader.fieldnames or 'performance' not in reader.fieldnames: # type: ignore
                raise Exception(f"Ошибка: в файле {filename} отсутствуют обязательные столбцы 'position' или 'performance'")
                
            for row in reader:
                cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
                
                employees.append(cleaned_row)

    return employees


def performance_report(employees: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """ Отчёт: средняя эффективность по позициям """
    # Группируем позиции и все значения эффективности сотрудников
    position_stats = defaultdict(list)
    for employee in employees:
        try:
            perf = float(employee['performance'])
            position = employee['position']
            position_stats[position].append(perf) 
        except ValueError:
            continue  # пропускаем некорректные значения

    result = []
    for position, performances in position_stats.items():
        avg_perf = sum(performances) / len(performances)
        result.append({
            'Position': position,
            'Avg Performance': round(avg_perf, 2)
        })
    
    # Сортировка по убыванию средней эффективности
    return sorted(result, key=lambda x: x['Avg Performance'], reverse=True)


# Для возможного расширения
REPORTS: Dict[str, Callable] = {
    'performance': performance_report
}

def print_report(report_name: str, data: List[Dict[str, Any]]) -> None:
    """ Выводит таблицу с отчётом """
    headers = data[0].keys()
    rows = [[i+1,*[row[h] for h in headers]] for i,row in enumerate(data)] # Форматирование словарей для вывода
    print(f"Отчёт: {report_name}")
    print(tabulate(rows,headers=list(headers), floatfmt=".2f"))

if __name__ == '__main__':
    main()