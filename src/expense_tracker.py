"""
CLI Expense Tracker Core Module

Цей модуль реалізує:
- Парсинг CLI-команд (add, report)
- Збереження та завантаження витрат у JSON
- Агрегацію витрат за категоріями

Структура запису витрати:
{
    "id": "uuid4-string",
    "date": "YYYY-MM-DD",
    "category": "string",
    "amount": float,
    "description": "string"
}
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from typing import List, Dict, Any

# Шлях до файлу з даними
DATA_FILE = "expenses.json"


# =========================
# Робота з даними (JSON)
# =========================

def load_expenses(file_path: str = DATA_FILE) -> List[Dict[str, Any]]:
    """
    Завантажує список витрат із JSON-файлу.

    :param file_path: шлях до JSON-файлу
    :return: список витрат
    """
    if not os.path.exists(file_path):
        # Якщо файл не існує — повертаємо пустий список
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("JSON структура повинна бути списком")

            return data

    except json.JSONDecodeError:
        print("Помилка: файл JSON пошкоджений.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Помилка при завантаженні даних: {e}", file=sys.stderr)
        return []


def save_expenses(expenses: List[Dict[str, Any]], file_path: str = DATA_FILE) -> None:
    """
    Зберігає список витрат у JSON-файл.

    :param expenses: список витрат
    :param file_path: шлях до JSON-файлу
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Помилка при збереженні даних: {e}", file=sys.stderr)


# =========================
# Бізнес-логіка
# =========================

def add_expense(amount: float, category: str, description: str, date: str = None) -> None:
    """
    Додає нову витрату до файлу.

    :param amount: сума витрати
    :param category: категорія
    :param description: опис
    :param date: дата у форматі YYYY-MM-DD (опціонально, за замовчуванням - поточна дата)
    """
    expenses = load_expenses()

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "id": str(uuid.uuid4()),
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Витрату додано успішно.")


def filter_expenses(expenses: List[Dict[str, Any]], category: str = None, 
                    start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """
    Фільтрує витрати за категорією та діапазоном дат.

    :param expenses: список витрат
    :param category: категорія для фільтрації (точне совпадение, опціонально)
    :param start_date: початкова дата у форматі YYYY-MM-DD (опціонально, включаючи)
    :param end_date: кінцева дата у форматі YYYY-MM-DD (опціонально, включаючи)
    :return: відфільтрований список витрат
    """
    filtered = expenses

    # Фільтрація за категорією
    if category is not None:
        filtered = [e for e in filtered if e.get("category") == category]

    # Фільтрація за діапазоном дат
    if start_date is not None:
        filtered = [e for e in filtered if e.get("date", "") >= start_date]

    if end_date is not None:
        filtered = [e for e in filtered if e.get("date", "") <= end_date]

    return filtered


def aggregate_by_category(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Агрегує витрати за категоріями.

    :param expenses: список витрат
    :return: словник {категорія: загальна сума}
    """
    result: Dict[str, float] = {}

    for expense in expenses:
        category = expense.get("category", "Unknown")
        amount = float(expense.get("amount", 0))

        if category not in result:
            result[category] = 0.0

        result[category] += amount

    return result


def generate_report() -> None:
    """
    Генерує та виводить звіт по витратах.
    """
    expenses = load_expenses()

    if not expenses:
        print("Немає даних для відображення.")
        return

    aggregated = aggregate_by_category(expenses)

    print("\nЗвіт по витратах:")
    print("-" * 30)

    for category, total in aggregated.items():
        print(f"{category}: {total:.2f}")

    print("-" * 30)
    print(f"Загалом: {sum(aggregated.values()):.2f}")


def display_expenses(expenses: List[Dict[str, Any]]) -> None:
    """
    Виводить список витрат у читаному форматі таблиці.

    :param expenses: список витрат для відображення
    """
    if not expenses:
        print("Немає витрат для відображення.")
        return

    print("\nСписок витрат:")

    # Column widths
    col_date = 12
    col_category = 15
    col_amount = 12
    col_description = 35

    # Calculate total width
    total_width = col_date + col_category + col_amount + col_description + 7  # +7 for separators

    # Header
    print("─" * total_width)
    print(f"{'Дата':<{col_date}} │ {'Категорія':<{col_category}} │ {'Сума':<{col_amount}} │ {'Опис':<{col_description}}")
    print("─" * total_width)

    total_amount = 0.0
    for expense in expenses:
        date = expense.get("date", "N/A")
        category = expense.get("category", "Unknown")
        amount = float(expense.get("amount", 0))
        description = expense.get("description", "")

        # Truncate long descriptions
        if len(description) > col_description - 1:
            description = description[:col_description - 4] + "..."

        # Format amount with 2 decimal places
        amount_str = f"${amount:,.2f}"

        print(f"{date:<{col_date}} │ {category:<{col_category}} │ {amount_str:>{col_amount}} │ {description:<{col_description}}")
        total_amount += amount

    print("─" * total_width)
    total_str = f"${total_amount:,.2f}"
    print(f"{'Загалом:':<{col_date}} │ {'':<{col_category}} │ {total_str:>{col_amount}} │ ({len(expenses)} витрат)")
    print("─" * total_width)



# =========================
# CLI (argparse)
# =========================

def create_parser() -> argparse.ArgumentParser:
    """
    Створює CLI-парсер з командами.

    :return: налаштований ArgumentParser
    """
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда add
    add_parser = subparsers.add_parser("add", help="Додати витрату")
    add_parser.add_argument("--amount", type=float, required=True, help="Сума витрати")
    add_parser.add_argument("--category", type=str, required=True, help="Категорія")
    add_parser.add_argument("--description", type=str, default="", help="Опис")
    add_parser.add_argument("--date", type=str, default=None, help="Дата у форматі YYYY-MM-DD (опціонально)")

    # Команда list
    list_parser = subparsers.add_parser("list", help="Показати список витрат")
    list_parser.add_argument("--category", type=str, default=None, help="Фільтрувати за категорією")
    list_parser.add_argument("--start-date", type=str, default=None, help="Початкова дата у форматі YYYY-MM-DD")
    list_parser.add_argument("--end-date", type=str, default=None, help="Кінцева дата у форматі YYYY-MM-DD")

    # Команда report
    subparsers.add_parser("report", help="Показати звіт")

    return parser


def main():
    """
    Точка входу CLI.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add":
        if args.amount <= 0:
            print("Сума повинна бути більшою за 0.", file=sys.stderr)
            sys.exit(1)

        # Валідація дати, якщо вона була надана
        if args.date is not None:
            try:
                datetime.strptime(args.date, "%Y-%m-%d")
            except ValueError:
                print("Помилка: невірний формат дати. Використовуйте YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)

        add_expense(args.amount, args.category, args.description, args.date)

    elif args.command == "list":
        # Валідація дат, якщо вони були надані
        if args.start_date is not None:
            try:
                datetime.strptime(args.start_date, "%Y-%m-%d")
            except ValueError:
                print("Помилка: невірний формат початкової дати. Використовуйте YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)

        if args.end_date is not None:
            try:
                datetime.strptime(args.end_date, "%Y-%m-%d")
            except ValueError:
                print("Помилка: невірний формат кінцевої дати. Використовуйте YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)

        expenses = load_expenses()
        filtered = filter_expenses(expenses, category=args.category, 
                                  start_date=args.start_date, end_date=args.end_date)
        display_expenses(filtered)

    elif args.command == "report":
        generate_report()


if __name__ == "__main__":
    main()