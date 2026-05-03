## Промпт до ChatGPT GPT-5.3

Ти — Senior Python Developer з великим досвідом розробки CLI-інструментів та архітектури систем. Я працюю над навчальним проектом "CLI Expense Tracker". Це консольна утиліта, яка дозволяє користувачам керувати своїми фінансами. Мені потрібно реалізувати ядро програми: обробку команд користувача та механізм збереження даних. Напиши Python-модуль, який включає: Парсинг аргументів командного рядка: реалізуй команди add (з параметрами --amount, --category, --description) та report (для перегляду статистики). Роботу з даними: функції для завантаження та збереження списку витрат у файл expenses.json. Агрегацію: функцію, яка приймає список витрат і повертає словник із загальними сумами для кожної категорії. Використовуй тільки стандартну бібліотеку argparse для CLI. Дані в JSON повинні мати чітку структуру: дата, категорія, сума, опис. Додай обробку помилок (наприклад, якщо файл JSON відсутній або пошкоджений). В результаті видай: Повний код файлу з детальними коментарями (Docstrings). Коротке пояснення логіки агрегації даних. Приклади того, як викликати ці функції в коді.


## Відповідь

Нижче наведено повний приклад Python-модуля для CLI Expense Tracker з використанням лише стандартної бібліотеки (`argparse`, `json`, `datetime`, `os`, `sys`).

---

# 📁 `expense_tracker.py`

```python
"""
CLI Expense Tracker Core Module

Цей модуль реалізує:
- Парсинг CLI-команд (add, report)
- Збереження та завантаження витрат у JSON
- Агрегацію витрат за категоріями

Структура запису витрати:
{
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

def add_expense(amount: float, category: str, description: str) -> None:
    """
    Додає нову витрату до файлу.

    :param amount: сума витрати
    :param category: категорія
    :param description: опис
    """
    expenses = load_expenses()

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Витрату додано успішно.")


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

        add_expense(args.amount, args.category, args.description)

    elif args.command == "report":
        generate_report()


if __name__ == "__main__":
    main()
```

/ ---

# 🧠 Пояснення логіки агрегації

Функція `aggregate_by_category` проходить по списку витрат і:

1. Для кожної витрати отримує категорію та суму
2. Якщо категорія ще не зустрічалась — створює її в словнику
3. Додає суму витрати до відповідної категорії

Результат:

```python
{
    "Food": 250.0,
    "Transport": 120.0
}
```

Це класичний reduce/accumulate підхід з часовою складністю **O(n)**.

/ ---

# ▶️ Приклади використання

## 1. Через CLI

```bash
# Додати витрату
python expense_tracker.py add --amount 100 --category Food --description "Lunch"

# Показати звіт
python expense_tracker.py report
```

/ ---

## 2. Виклик функцій у коді

```python
from expense_tracker import (
    load_expenses,
    save_expenses,
    aggregate_by_category,
    add_expense
)

# Додати витрату
add_expense(50, "Transport", "Bus ticket")

# Завантажити дані
expenses = load_expenses()

# Агрегація
stats = aggregate_by_category(expenses)
print(stats)
```

/ ---

Якщо потрібно — можу розширити архітектуру (наприклад: додати фільтрацію по даті, dependency injection для сховища, або перехід на layered design).


---


## Промпти до GitHub Copilot моделі Claude Haiku 4.5
### 1
Add a unique "id" field to each expense using uuid4.

Requirements:
- Import uuid
- Generate id when adding a new expense
- Ensure all existing code continues to work
- Update data structure accordingly

### 2
Extend the CLI "add" command to accept optional --date argument.

Requirements:
- Format: YYYY-MM-DD
- Validate using datetime.strptime
- If not provided, fallback to current date
- Show error and exit if invalid format

### 3
Implement filtering functionality for expenses.

Requirements:
- Create function filter_expenses(expenses, category=None, start_date=None, end_date=None)
- Filter by:
  - category (exact match)
  - date range (inclusive)
- Dates are strings in YYYY-MM-DD format
- Return filtered list

### 4
Add a new CLI command "list" to display expenses.

Requirements:
- Show all expenses
- Support optional filters:
  --category
  --start-date
  --end-date
- Reuse filter_expenses function
- Print results in readable format

### 5
Improve CLI output formatting.

Requirements:
- Align columns for list output
- Show:
  date | category | amount | description
- Format amount to 2 decimal places

## 
---


