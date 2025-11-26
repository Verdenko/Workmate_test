# tests/test_main.py

import pytest
import sys
import argparse
from pathlib import Path
from src.main import (
    validate_file_extension,
    read_employees_from_files,
    performance_report,
    main,
)

DATA_DIR = Path(__file__).parent / "data"

EMP1 = str(DATA_DIR / "employees1.csv")
EMP2 = str(DATA_DIR / "employees2.csv")
EMPTY = str(DATA_DIR / "empty_employees.csv")
MISSING = str(DATA_DIR / "missing_column.csv")

def test_validate_file_extension():
    assert validate_file_extension("file.csv") == "file.csv"
    with pytest.raises(argparse.ArgumentTypeError):
        validate_file_extension("file.txt")


def test_read_employees_from_one_file():
    employees = read_employees_from_files([EMP1])
    assert len(employees) == 9
    assert employees[0]["name"] == "David Chen"
    assert employees[0]["position"] == "Mobile Developer"
    assert employees[6]["performance"] == "4.9"


def test_read_employees_from_two_files():
    employees = read_employees_from_files([EMP1, EMP2])
    positions = {e["position"] for e in employees}
    assert "Fullstack Developer" in positions
    assert "Data Scientist" in positions

def test_read_missing_column():
    """Проверяем, что срабатывает именно эта строчка кода"""
    with pytest.raises(Exception) as exception:
        read_employees_from_files([MISSING])
    
    error_msg = str(exception.value)
    assert "missing_column.csv" in error_msg
    assert "отсутствуют обязательные столбцы" in error_msg
    assert "performance" in error_msg
    assert "position" in error_msg or "performance" in error_msg

def test_read_empty_file():
    employees = read_employees_from_files([EMPTY])
    assert employees == []


def test_performance_report():
    employees = read_employees_from_files([EMP1, EMP2])
    result = performance_report(employees)

    assert result[0]["Position"] == "Backend Developer"
    assert result[0]["Avg Performance"] == 4.83  # (4.8 + 4.8 + 4.9)/3 ≈ 4.83
    assert result[1]["Position"] == "DevOps Engineer"
    assert result[1]["Avg Performance"] == 4.8  # (4.7 + 4.9)/2 = 4.8

def test_main_with_empty_file(capsys):
    original_argv = sys.argv
    sys.argv = ["main.py", "--files", EMPTY, "--report", "performance"]

    try:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    finally:
        sys.argv = original_argv

    output = capsys.readouterr().out
    assert "Не удалось прочитать данные из файлов." in output
    assert "Ошибка: В файле нет данных сотрудников." in output
    assert "usage:" in output


def test_main(capsys):
    original_argv = sys.argv
    sys.argv = ["main.py", "--files", EMP1, EMP2, "--report", "performance"]

    try:
        main()
    finally:
        sys.argv = original_argv

    output = capsys.readouterr().out

    assert "Отчёт: performance" in output
    assert "Backend Developer" in output
    assert "4.83" in output
    assert "DevOps Engineer" in output
    assert "4.80" in output
    assert "1  Backend Developer" in output
    assert "2  DevOps Engineer" in output

