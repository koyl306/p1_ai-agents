#!/usr/bin/env python3
"""
Test filter_expenses function
"""

import sys
sys.path.insert(0, '.')

from expense_tracker import filter_expenses

# Sample test data
sample_expenses = [
    {
        "id": "uuid-1",
        "date": "2024-01-10",
        "category": "Food",
        "amount": 25.50,
        "description": "Lunch"
    },
    {
        "id": "uuid-2",
        "date": "2024-01-15",
        "category": "Transport",
        "amount": 10.00,
        "description": "Bus fare"
    },
    {
        "id": "uuid-3",
        "date": "2024-01-20",
        "category": "Food",
        "amount": 35.00,
        "description": "Dinner"
    },
    {
        "id": "uuid-4",
        "date": "2024-02-05",
        "category": "Food",
        "amount": 15.50,
        "description": "Breakfast"
    },
    {
        "id": "uuid-5",
        "date": "2024-02-10",
        "category": "Transport",
        "amount": 20.00,
        "description": "Taxi"
    },
]

def print_expenses(expenses, title):
    """Helper to print expenses"""
    print(f"\n{title}")
    print("-" * 60)
    if not expenses:
        print("No expenses found")
        return
    for exp in expenses:
        print(f"  {exp['date']} | {exp['category']:12} | ${exp['amount']:7.2f} | {exp['description']}")
    print(f"Total: ${sum(e['amount'] for e in expenses):.2f}")

# Test 1: Filter by category
print_expenses(
    filter_expenses(sample_expenses, category="Food"),
    "TEST 1: Filter by category='Food'"
)

# Test 2: Filter by date range
print_expenses(
    filter_expenses(sample_expenses, start_date="2024-01-15", end_date="2024-02-05"),
    "TEST 2: Filter by date range [2024-01-15 to 2024-02-05]"
)

# Test 3: Filter by category AND date range
print_expenses(
    filter_expenses(sample_expenses, category="Food", start_date="2024-01-01", end_date="2024-01-31"),
    "TEST 3: Filter by category='Food' AND date range [2024-01-01 to 2024-01-31]"
)

# Test 4: Filter with no criteria (should return all)
print_expenses(
    filter_expenses(sample_expenses),
    "TEST 4: No filter criteria (all expenses)"
)

# Test 5: Filter by start_date only
print_expenses(
    filter_expenses(sample_expenses, start_date="2024-02-01"),
    "TEST 5: Filter by start_date='2024-02-01' (inclusive)"
)

# Test 6: Filter by end_date only
print_expenses(
    filter_expenses(sample_expenses, end_date="2024-01-20"),
    "TEST 6: Filter by end_date='2024-01-20' (inclusive)"
)

# Test 7: No matching results
print_expenses(
    filter_expenses(sample_expenses, category="Utilities"),
    "TEST 7: No matching category='Utilities'"
)

# Test 8: Empty date range
print_expenses(
    filter_expenses(sample_expenses, start_date="2024-03-01", end_date="2024-03-31"),
    "TEST 8: Empty date range [2024-03-01 to 2024-03-31]"
)

print("\n" + "=" * 60)
print("✓ All filter tests completed successfully!")
print("=" * 60)
